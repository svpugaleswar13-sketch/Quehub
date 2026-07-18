from datetime import date, datetime

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app import models, schemas
from app.database import get_db
from app.deps import require_customer
from app.queue_utils import (
    queue_snapshot, get_current_serving_number, get_available_token_numbers,
    count_waiting_ahead, estimate_wait_minutes,
)
from app.ws_manager import manager

router = APIRouter(tags=["customer"])


# ---------- Browse ----------

@router.get("/domains", response_model=list[str])
def list_domains(db: Session = Depends(get_db)):
    rows = db.query(models.Organization.domain).distinct().all()
    return sorted({r[0] for r in rows}) or [
        "Hospital", "Bank", "Salon", "Spa", "Government Office", "Passport Office", "Vehicle Service Center",
    ]


@router.get("/organizations", response_model=list[schemas.OrganizationOut])
def list_organizations(domain: str | None = None, db: Session = Depends(get_db)):
    query = db.query(models.Organization)
    if domain:
        query = query.filter(models.Organization.domain == domain)
    return query.all()


@router.get("/organizations/{organization_id}", response_model=schemas.OrganizationOut)
def get_organization(organization_id: str, db: Session = Depends(get_db)):
    org = db.query(models.Organization).filter(models.Organization.id == organization_id).first()
    if not org:
        raise HTTPException(status_code=404, detail="Organization not found")
    return org


@router.get("/organizations/{organization_id}/services", response_model=list[schemas.ServiceOut])
def list_services(organization_id: str, db: Session = Depends(get_db)):
    return (
        db.query(models.Service)
        .filter(models.Service.organization_id == organization_id, models.Service.is_active.is_(True))
        .all()
    )


@router.get("/services/{service_id}", response_model=schemas.ServiceDetailOut)
def get_service_detail(service_id: str, db: Session = Depends(get_db)):
    service = db.query(models.Service).filter(models.Service.id == service_id).first()
    if not service:
        raise HTTPException(status_code=404, detail="Service not found")

    snap = queue_snapshot(db, service)
    customers_ahead = snap["booked_tokens"]  # rough estimate for the "next" token
    return schemas.ServiceDetailOut(
        service=schemas.ServiceOut.model_validate(service),
        current_token=snap["current_token"],
        booked_tokens=snap["booked_tokens"],
        available_tokens=snap["available_tokens"],
        available_token_numbers=snap["available_token_numbers"],
        estimated_waiting_time_minutes=estimate_wait_minutes(customers_ahead, service.average_service_time),
    )


# ---------- Booking ----------

@router.post("/services/{service_id}/book", response_model=schemas.BookingSuccessOut, status_code=status.HTTP_201_CREATED)
async def book_token(
    service_id: str,
    payload: schemas.BookTokenRequest,
    db: Session = Depends(get_db),
    customer: models.User = Depends(require_customer),
):
    service = db.query(models.Service).filter(models.Service.id == service_id, models.Service.is_active.is_(True)).first()
    if not service:
        raise HTTPException(status_code=404, detail="Service not found")

    if not (1 <= payload.token_number <= service.max_tokens):
        raise HTTPException(status_code=400, detail="Invalid token number for this service")

    today = date.today()

    # FCFS is enforced by the DB unique constraint on (service_id, date, token_number).
    # If two requests race for the same token, only the first INSERT succeeds.
    new_token = models.Token(
        service_id=service.id,
        date=today,
        token_number=payload.token_number,
        customer_id=customer.id,
        customer_name=customer.name,
        status=models.TokenStatus.waiting,
        is_walk_in=False,
    )
    db.add(new_token)
    try:
        db.flush()
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Token {payload.token_number} has just been booked by another customer. Please choose another available token.",
        )

    customers_ahead = count_waiting_ahead(db, service.id, today, payload.token_number)
    wait_minutes = estimate_wait_minutes(customers_ahead, service.average_service_time)

    booking = models.Booking(
        customer_id=customer.id,
        token_id=new_token.id,
        estimated_time=datetime.utcnow(),
        status=models.BookingStatus.waiting,
    )
    db.add(booking)

    notification = models.Notification(
        customer_id=customer.id,
        message=f"Token {payload.token_number} booked for {service.name}. Estimated wait: {wait_minutes} minutes.",
    )
    db.add(notification)

    db.commit()
    db.refresh(new_token)

    current = get_current_serving_number(db, service.id, today)
    org = db.query(models.Organization).filter(models.Organization.id == service.organization_id).first()

    await manager.broadcast(service.id, queue_snapshot(db, service))

    return schemas.BookingSuccessOut(
        organization_name=org.name if org else "",
        service_name=service.name,
        token_number=payload.token_number,
        current_token=current,
        customers_before_you=customers_ahead,
        estimated_waiting_time_minutes=wait_minutes,
        estimated_arrival_time=datetime.utcnow(),
        status=booking.status,
    )


@router.get("/services/{service_id}/live-queue")
def live_queue_snapshot(service_id: str, db: Session = Depends(get_db)):
    service = db.query(models.Service).filter(models.Service.id == service_id).first()
    if not service:
        raise HTTPException(status_code=404, detail="Service not found")
    return queue_snapshot(db, service)


# ---------- History ----------

@router.get("/bookings/history", response_model=list[schemas.BookingHistoryOut])
def booking_history(db: Session = Depends(get_db), customer: models.User = Depends(require_customer)):
    bookings = (
        db.query(models.Booking)
        .filter(models.Booking.customer_id == customer.id)
        .order_by(models.Booking.created_at.desc())
        .all()
    )
    results = []
    for b in bookings:
        token = b.token
        service = token.service
        org = service.organization
        results.append(schemas.BookingHistoryOut(
            booking_id=b.id,
            organization_name=org.name,
            service_name=service.name,
            token_number=token.token_number,
            status=b.status,
            booking_time=token.booking_time,
            service_id=service.id,
        ))
    return results


# ---------- Notifications ----------

@router.get("/notifications", response_model=list[schemas.NotificationOut])
def list_notifications(db: Session = Depends(get_db), customer: models.User = Depends(require_customer)):
    return (
        db.query(models.Notification)
        .filter(models.Notification.customer_id == customer.id)
        .order_by(models.Notification.created_at.desc())
        .all()
    )


@router.post("/notifications/{notification_id}/read", response_model=schemas.NotificationOut)
def mark_notification_read(notification_id: str, db: Session = Depends(get_db), customer: models.User = Depends(require_customer)):
    notif = (
        db.query(models.Notification)
        .filter(models.Notification.id == notification_id, models.Notification.customer_id == customer.id)
        .first()
    )
    if not notif:
        raise HTTPException(status_code=404, detail="Notification not found")
    notif.read_status = True
    db.commit()
    db.refresh(notif)
    return notif

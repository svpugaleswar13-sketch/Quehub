from datetime import date, datetime, time as time_type

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import func
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app import models, schemas
from app.database import get_db
from app.deps import require_organization
from app.queue_utils import queue_snapshot, get_current_serving_number, count_waiting_ahead, estimate_wait_minutes
from app.ws_manager import manager

router = APIRouter(prefix="/organization", tags=["organization"])


def get_org_for_user(db: Session, user: models.User) -> models.Organization:
    org = db.query(models.Organization).filter(models.Organization.owner_id == user.id).first()
    if not org:
        raise HTTPException(status_code=404, detail="No organization profile found for this account")
    return org


def get_own_service(db: Session, service_id: str, org: models.Organization) -> models.Service:
    service = (
        db.query(models.Service)
        .filter(models.Service.id == service_id, models.Service.organization_id == org.id)
        .first()
    )
    if not service:
        raise HTTPException(status_code=404, detail="Service not found for this organization")
    return service


# ---------- Dashboard ----------

@router.get("/dashboard", response_model=schemas.DashboardStatsOut)
def dashboard(db: Session = Depends(get_db), user: models.User = Depends(require_organization)):
    org = get_org_for_user(db, user)
    today = date.today()
    service_ids = [s.id for s in org.services]

    base_query = db.query(models.Token).filter(models.Token.service_id.in_(service_ids), models.Token.date == today)

    todays_bookings = base_query.count()
    completed = base_query.filter(models.Token.status == models.TokenStatus.completed).count()
    cancelled = base_query.filter(models.Token.status == models.TokenStatus.cancelled).count()
    pending = base_query.filter(models.Token.status.in_([models.TokenStatus.waiting, models.TokenStatus.serving])).count()

    current_token = None
    if service_ids:
        serving = base_query.filter(models.Token.status == models.TokenStatus.serving).order_by(models.Token.token_number.desc()).first()
        current_token = serving.token_number if serving else None

    avg_service_time = 0
    if org.services:
        avg_service_time = round(sum(s.average_service_time for s in org.services) / len(org.services))

    return schemas.DashboardStatsOut(
        todays_bookings=todays_bookings,
        current_token=current_token,
        completed_tokens=completed,
        pending_tokens=pending,
        cancelled_tokens=cancelled,
        average_waiting_time_minutes=avg_service_time,
    )


# ---------- Queue management ----------

@router.get("/queue/{service_id}")
def get_queue(service_id: str, db: Session = Depends(get_db), user: models.User = Depends(require_organization)):
    org = get_org_for_user(db, user)
    service = get_own_service(db, service_id, org)
    return queue_snapshot(db, service, anonymize=False)



@router.post("/queue/{service_id}/call-next")
async def call_next(service_id: str, db: Session = Depends(get_db), user: models.User = Depends(require_organization)):
    org = get_org_for_user(db, user)
    service = get_own_service(db, service_id, org)
    today = date.today()

    currently_serving = (
        db.query(models.Token)
        .filter(models.Token.service_id == service.id, models.Token.date == today, models.Token.status == models.TokenStatus.serving)
        .first()
    )
    if currently_serving:
        raise HTTPException(status_code=400, detail="Complete or skip the current token before calling the next one")

    next_token = (
        db.query(models.Token)
        .filter(models.Token.service_id == service.id, models.Token.date == today, models.Token.status == models.TokenStatus.waiting)
        .order_by(models.Token.token_number.asc())
        .first()
    )
    if not next_token:
        raise HTTPException(status_code=404, detail="No waiting tokens in the queue")

    next_token.status = models.TokenStatus.serving
    db.commit()

    await manager.broadcast(service.id, queue_snapshot(db, service))
    return {"token_number": next_token.token_number, "status": next_token.status.value}


@router.post("/queue/{service_id}/skip")
async def skip_current(service_id: str, db: Session = Depends(get_db), user: models.User = Depends(require_organization)):
    org = get_org_for_user(db, user)
    service = get_own_service(db, service_id, org)
    today = date.today()

    current = (
        db.query(models.Token)
        .filter(models.Token.service_id == service.id, models.Token.date == today, models.Token.status == models.TokenStatus.serving)
        .first()
    )
    if not current:
        raise HTTPException(status_code=404, detail="No token is currently being served")

    current.status = models.TokenStatus.skipped
    db.commit()

    await manager.broadcast(service.id, queue_snapshot(db, service))
    return {"token_number": current.token_number, "status": current.status.value}


@router.post("/queue/{service_id}/complete")
async def complete_current(service_id: str, db: Session = Depends(get_db), user: models.User = Depends(require_organization)):
    org = get_org_for_user(db, user)
    service = get_own_service(db, service_id, org)
    today = date.today()

    current = (
        db.query(models.Token)
        .filter(models.Token.service_id == service.id, models.Token.date == today, models.Token.status == models.TokenStatus.serving)
        .first()
    )
    if not current:
        raise HTTPException(status_code=404, detail="No token is currently being served")

    current.status = models.TokenStatus.completed
    if current.booking:
        current.booking.status = models.BookingStatus.completed
    db.commit()

    await manager.broadcast(service.id, queue_snapshot(db, service))
    return {"token_number": current.token_number, "status": current.status.value}


# ---------- Walk-in booking ----------

@router.post("/walk-in", response_model=schemas.TokenOut, status_code=status.HTTP_201_CREATED)
async def walk_in_booking(payload: schemas.WalkInBookingRequest, db: Session = Depends(get_db), user: models.User = Depends(require_organization)):
    org = get_org_for_user(db, user)
    service = get_own_service(db, payload.service_id, org)

    if not (1 <= payload.token_number <= service.max_tokens):
        raise HTTPException(status_code=400, detail="Invalid token number for this service")

    today = date.today()
    new_token = models.Token(
        service_id=service.id,
        date=today,
        token_number=payload.token_number,
        customer_id=None,
        customer_name=payload.customer_name,
        customer_phone=payload.customer_phone,
        status=models.TokenStatus.waiting,
        is_walk_in=True,
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
    db.commit()
    db.refresh(new_token)

    await manager.broadcast(service.id, queue_snapshot(db, service))
    return new_token


# ---------- Manage services ----------

@router.get("/services", response_model=list[schemas.ServiceOut])
def list_own_services(db: Session = Depends(get_db), user: models.User = Depends(require_organization)):
    org = get_org_for_user(db, user)
    return org.services


@router.post("/services", response_model=schemas.ServiceOut, status_code=status.HTTP_201_CREATED)
def create_service(payload: schemas.ServiceCreate, db: Session = Depends(get_db), user: models.User = Depends(require_organization)):
    org = get_org_for_user(db, user)
    service = models.Service(organization_id=org.id, **payload.model_dump())
    db.add(service)
    db.commit()
    db.refresh(service)
    return service


@router.put("/services/{service_id}", response_model=schemas.ServiceOut)
def update_service(service_id: str, payload: schemas.ServiceUpdate, db: Session = Depends(get_db), user: models.User = Depends(require_organization)):
    org = get_org_for_user(db, user)
    service = get_own_service(db, service_id, org)
    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(service, field, value)
    db.commit()
    db.refresh(service)
    return service


@router.delete("/services/{service_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_service(service_id: str, db: Session = Depends(get_db), user: models.User = Depends(require_organization)):
    org = get_org_for_user(db, user)
    service = get_own_service(db, service_id, org)
    db.delete(service)
    db.commit()
    return None


# ---------- Reports ----------

@router.get("/reports", response_model=schemas.ReportsOut)
def reports(db: Session = Depends(get_db), user: models.User = Depends(require_organization)):
    org = get_org_for_user(db, user)
    today = date.today()
    service_ids = [s.id for s in org.services]

    base_query = db.query(models.Token).filter(models.Token.service_id.in_(service_ids), models.Token.date == today)
    todays_bookings = base_query.count()
    completed = base_query.filter(models.Token.status == models.TokenStatus.completed).count()
    cancelled = base_query.filter(models.Token.status == models.TokenStatus.cancelled).count()

    avg_service_time = 0
    if org.services:
        avg_service_time = round(sum(s.average_service_time for s in org.services) / len(org.services))

    most_booked = (
        db.query(models.Service.name, func.count(models.Token.id).label("cnt"))
        .join(models.Token, models.Token.service_id == models.Service.id)
        .filter(models.Service.organization_id == org.id, models.Token.date == today)
        .group_by(models.Service.name)
        .order_by(func.count(models.Token.id).desc())
        .first()
    )

    peak_hour_row = (
        db.query(func.extract("hour", models.Token.booking_time).label("hr"), func.count(models.Token.id).label("cnt"))
        .filter(models.Token.service_id.in_(service_ids), models.Token.date == today)
        .group_by("hr")
        .order_by(func.count(models.Token.id).desc())
        .first()
    )

    return schemas.ReportsOut(
        todays_bookings=todays_bookings,
        completed_tokens=completed,
        cancelled_tokens=cancelled,
        average_waiting_time_minutes=avg_service_time,
        most_booked_service=most_booked[0] if most_booked else None,
        peak_hour=f"{int(peak_hour_row[0]):02d}:00" if peak_hour_row else None,
    )

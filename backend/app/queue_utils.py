from datetime import date, datetime, timedelta
from typing import Optional

from sqlalchemy import func
from sqlalchemy.orm import Session

from app import models


def get_current_serving_number(db: Session, service_id: str, on_date: date) -> Optional[int]:
    """The token currently being served (or the last completed one if none is
    actively 'serving' right now — used to seed the display)."""
    serving = (
        db.query(models.Token)
        .filter(models.Token.service_id == service_id, models.Token.date == on_date,
                models.Token.status == models.TokenStatus.serving)
        .order_by(models.Token.token_number.desc())
        .first()
    )
    if serving:
        return serving.token_number

    last_completed = (
        db.query(models.Token)
        .filter(models.Token.service_id == service_id, models.Token.date == on_date,
                models.Token.status == models.TokenStatus.completed)
        .order_by(models.Token.token_number.desc())
        .first()
    )
    return last_completed.token_number if last_completed else 0


def get_booked_token_numbers(db: Session, service_id: str, on_date: date) -> set:
    rows = (
        db.query(models.Token.token_number)
        .filter(
            models.Token.service_id == service_id,
            models.Token.date == on_date,
            models.Token.status.in_([
                models.TokenStatus.waiting, models.TokenStatus.serving, models.TokenStatus.completed
            ]),
        )
        .all()
    )
    return {r[0] for r in rows}


def get_available_token_numbers(db: Session, service: models.Service, on_date: date) -> list[int]:
    booked = get_booked_token_numbers(db, service.id, on_date)
    return [n for n in range(1, service.max_tokens + 1) if n not in booked]


def count_waiting_ahead(db: Session, service_id: str, on_date: date, token_number: int) -> int:
    """How many waiting/serving tokens have a lower number than this one."""
    return (
        db.query(func.count(models.Token.id))
        .filter(
            models.Token.service_id == service_id,
            models.Token.date == on_date,
            models.Token.token_number < token_number,
            models.Token.status.in_([models.TokenStatus.waiting, models.TokenStatus.serving]),
        )
        .scalar()
        or 0
    )


def estimate_wait_minutes(customers_ahead: int, average_service_time: int) -> int:
    return max(customers_ahead, 0) * average_service_time


def queue_snapshot(db: Session, service: models.Service, on_date: Optional[date] = None, anonymize: bool = True) -> dict:
    """Full snapshot of a service's queue state — used both for REST responses
    and for the payload broadcast over WebSockets whenever the queue changes."""
    on_date = on_date or date.today()
    current = get_current_serving_number(db, service.id, on_date)
    booked = get_booked_token_numbers(db, service.id, on_date)
    available = get_available_token_numbers(db, service, on_date)

    tokens_query = db.query(models.Token).filter(models.Token.service_id == service.id, models.Token.date == on_date)
    if anonymize:
        tokens_query = tokens_query.filter(models.Token.status.in_([models.TokenStatus.waiting, models.TokenStatus.serving]))
    waiting_tokens = tokens_query.order_by(models.Token.token_number.asc()).all()

    return {
        "service_id": service.id,
        "service_name": service.name,
        "current_token": current,
        "max_tokens": service.max_tokens,
        "booked_tokens": len(booked),
        "available_tokens": len(available),
        "available_token_numbers": available,
        "average_service_time": service.average_service_time,
        "queue": [
            {
                "token_id": t.id,
                "token_number": t.token_number,
                "status": t.status.value,
                "customer_name": None if anonymize else t.customer_name,
                "is_walk_in": t.is_walk_in,
            }
            for t in waiting_tokens
        ],
    }


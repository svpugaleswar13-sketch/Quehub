import enum
import uuid
from datetime import datetime, date as date_type

from sqlalchemy import (
    Column, String, Integer, Boolean, DateTime, Date, Time, ForeignKey,
    Enum as SAEnum, Text, UniqueConstraint, Numeric
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.database import Base


def gen_uuid():
    return str(uuid.uuid4())


class UserRole(str, enum.Enum):
    customer = "customer"
    organization = "organization"


class TokenStatus(str, enum.Enum):
    waiting = "waiting"
    serving = "serving"
    completed = "completed"
    skipped = "skipped"
    cancelled = "cancelled"


class BookingStatus(str, enum.Enum):
    waiting = "waiting"
    completed = "completed"
    cancelled = "cancelled"


class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=False), primary_key=True, default=gen_uuid)
    name = Column(String(150), nullable=False)
    email = Column(String(255), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    role = Column(SAEnum(UserRole), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    organization = relationship("Organization", back_populates="owner", uselist=False)
    bookings = relationship("Booking", back_populates="customer")
    notifications = relationship("Notification", back_populates="customer")


class Organization(Base):
    __tablename__ = "organizations"

    id = Column(UUID(as_uuid=False), primary_key=True, default=gen_uuid)
    owner_id = Column(UUID(as_uuid=False), ForeignKey("users.id"), nullable=False, unique=True)
    name = Column(String(200), nullable=False)
    domain = Column(String(100), nullable=False, index=True)  # Hospital, Bank, Salon, etc.
    address = Column(String(400))
    working_hours = Column(String(100))  # e.g. "09:00 AM - 05:00 PM"
    rating = Column(Numeric(2, 1), default=0)
    created_at = Column(DateTime, default=datetime.utcnow)

    owner = relationship("User", back_populates="organization")
    services = relationship("Service", back_populates="organization", cascade="all, delete-orphan")


class Service(Base):
    __tablename__ = "services"

    id = Column(UUID(as_uuid=False), primary_key=True, default=gen_uuid)
    organization_id = Column(UUID(as_uuid=False), ForeignKey("organizations.id"), nullable=False)
    name = Column(String(150), nullable=False)
    start_time = Column(Time, nullable=False)
    end_time = Column(Time, nullable=False)
    max_tokens = Column(Integer, nullable=False, default=50)
    average_service_time = Column(Integer, nullable=False, default=10)  # minutes
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    organization = relationship("Organization", back_populates="services")
    tokens = relationship("Token", back_populates="service", cascade="all, delete-orphan")


class Token(Base):
    """A single token slot for a service on a given day. Represents queue state."""
    __tablename__ = "tokens"
    __table_args__ = (
        UniqueConstraint("service_id", "date", "token_number", name="uq_token_slot"),
    )

    id = Column(UUID(as_uuid=False), primary_key=True, default=gen_uuid)
    service_id = Column(UUID(as_uuid=False), ForeignKey("services.id"), nullable=False)
    date = Column(Date, nullable=False, default=date_type.today)
    token_number = Column(Integer, nullable=False)
    customer_id = Column(UUID(as_uuid=False), ForeignKey("users.id"), nullable=True)
    customer_name = Column(String(150), nullable=True)  # used for walk-ins without an account
    customer_phone = Column(String(30), nullable=True)
    status = Column(SAEnum(TokenStatus), nullable=False, default=TokenStatus.waiting)
    is_walk_in = Column(Boolean, default=False)
    booking_time = Column(DateTime, default=datetime.utcnow)

    service = relationship("Service", back_populates="tokens")
    booking = relationship("Booking", back_populates="token", uselist=False)


class Booking(Base):
    """Customer-facing booking record tied to a token."""
    __tablename__ = "bookings"

    id = Column(UUID(as_uuid=False), primary_key=True, default=gen_uuid)
    customer_id = Column(UUID(as_uuid=False), ForeignKey("users.id"), nullable=False)
    token_id = Column(UUID(as_uuid=False), ForeignKey("tokens.id"), nullable=False, unique=True)
    estimated_time = Column(DateTime, nullable=True)  # estimated arrival/service time
    status = Column(SAEnum(BookingStatus), nullable=False, default=BookingStatus.waiting)
    created_at = Column(DateTime, default=datetime.utcnow)

    customer = relationship("User", back_populates="bookings")
    token = relationship("Token", back_populates="booking")


class Notification(Base):
    __tablename__ = "notifications"

    id = Column(UUID(as_uuid=False), primary_key=True, default=gen_uuid)
    customer_id = Column(UUID(as_uuid=False), ForeignKey("users.id"), nullable=False)
    message = Column(Text, nullable=False)
    read_status = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    customer = relationship("User", back_populates="notifications")

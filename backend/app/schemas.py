from datetime import datetime, date, time
import re
from typing import Optional, List

from pydantic import BaseModel, EmailStr, Field, field_validator, model_validator

from app.models import UserRole, TokenStatus, BookingStatus


# ---------- Auth ----------

class UserRegister(BaseModel):
    name: str
    email: EmailStr
    password: str = Field(min_length=6)
    role: UserRole
    # required only when role == organization
    organization_name: Optional[str] = None
    domain: Optional[str] = None
    address: Optional[str] = None
    working_hours: Optional[str] = None

    @field_validator('name')
    @classmethod
    def clean_name(cls, v: str) -> str:
        return v.strip()

    @field_validator('email')
    @classmethod
    def clean_email(cls, v: EmailStr) -> EmailStr:
        return str(v).strip().lower()

    @field_validator('organization_name')
    @classmethod
    def clean_org_name(cls, v: Optional[str]) -> Optional[str]:
        return v.strip() if v is not None else None

    @field_validator('address')
    @classmethod
    def clean_address(cls, v: Optional[str]) -> Optional[str]:
        return v.strip() if v is not None else None

    @field_validator('working_hours')
    @classmethod
    def clean_working_hours(cls, v: Optional[str]) -> Optional[str]:
        if v is None or v.strip() == "":
            return None
        cleaned = v.strip()
        pattern = r"^(0[1-9]|1[0-2]):[0-5][0-9]\s(AM|PM|am|pm)\s-\s(0[1-9]|1[0-2]):[0-5][0-9]\s(AM|PM|am|pm)$"
        if not re.match(pattern, cleaned):
            raise ValueError("Working hours must be in the format 'HH:MM AM/PM - HH:MM AM/PM' (e.g., 09:00 AM - 05:00 PM)")
        return cleaned


class UserLogin(BaseModel):
    email: EmailStr
    password: str

    @field_validator('email')
    @classmethod
    def clean_email(cls, v: EmailStr) -> EmailStr:
        return str(v).strip().lower()


class UserOut(BaseModel):
    id: str
    name: str
    email: EmailStr
    role: UserRole

    class Config:
        from_attributes = True


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserOut


# ---------- Organization ----------

class OrganizationOut(BaseModel):
    id: str
    name: str
    domain: str
    address: Optional[str] = None
    working_hours: Optional[str] = None
    rating: Optional[float] = None

    class Config:
        from_attributes = True


class OrganizationUpdate(BaseModel):
    name: Optional[str] = None
    address: Optional[str] = None
    working_hours: Optional[str] = None

    @field_validator('name')
    @classmethod
    def clean_name(cls, v: Optional[str]) -> Optional[str]:
        return v.strip() if v is not None else None

    @field_validator('address')
    @classmethod
    def clean_address(cls, v: Optional[str]) -> Optional[str]:
        return v.strip() if v is not None else None

    @field_validator('working_hours')
    @classmethod
    def clean_working_hours(cls, v: Optional[str]) -> Optional[str]:
        if v is None or v.strip() == "":
            return None
        cleaned = v.strip()
        pattern = r"^(0[1-9]|1[0-2]):[0-5][0-9]\s(AM|PM|am|pm)\s-\s(0[1-9]|1[0-2]):[0-5][0-9]\s(AM|PM|am|pm)$"
        if not re.match(pattern, cleaned):
            raise ValueError("Working hours must be in the format 'HH:MM AM/PM - HH:MM AM/PM' (e.g., 09:00 AM - 05:00 PM)")
        return cleaned


# ---------- Service ----------

class ServiceCreate(BaseModel):
    name: str
    start_time: time
    end_time: time
    max_tokens: int = Field(gt=0)
    average_service_time: int = Field(gt=0)

    @field_validator('name')
    @classmethod
    def clean_name(cls, v: str) -> str:
        return v.strip()

    @model_validator(mode='after')
    def validate_times(self) -> 'ServiceCreate':
        if self.start_time >= self.end_time:
            raise ValueError("start_time must be before end_time")
        return self


class ServiceUpdate(BaseModel):
    name: Optional[str] = None
    start_time: Optional[time] = None
    end_time: Optional[time] = None
    max_tokens: Optional[int] = None
    average_service_time: Optional[int] = None
    is_active: Optional[bool] = None

    @field_validator('name')
    @classmethod
    def clean_name(cls, v: Optional[str]) -> Optional[str]:
        return v.strip() if v is not None else None

    @model_validator(mode='after')
    def validate_times(self) -> 'ServiceUpdate':
        if self.start_time is not None and self.end_time is not None:
            if self.start_time >= self.end_time:
                raise ValueError("start_time must be before end_time")
        return self


class ServiceOut(BaseModel):
    id: str
    organization_id: str
    name: str
    start_time: time
    end_time: time
    max_tokens: int
    average_service_time: int
    is_active: bool

    class Config:
        from_attributes = True


class ServiceDetailOut(BaseModel):
    service: ServiceOut
    current_token: Optional[int] = None
    booked_tokens: int
    available_tokens: int
    available_token_numbers: List[int]
    estimated_waiting_time_minutes: int


# ---------- Tokens / Booking ----------

class BookTokenRequest(BaseModel):
    token_number: int


class WalkInBookingRequest(BaseModel):
    customer_name: str
    customer_phone: Optional[str] = None
    service_id: str
    token_number: int

    @field_validator('customer_name')
    @classmethod
    def clean_customer_name(cls, v: str) -> str:
        return v.strip()

    @field_validator('customer_phone')
    @classmethod
    def clean_phone(cls, v: Optional[str]) -> Optional[str]:
        if v is None or v.strip() == "":
            return None
        cleaned = v.strip()
        digits_only = re.sub(r"[\s\-\(\)]", "", cleaned)
        if not re.match(r"^\+?[0-9]{10,15}$", digits_only):
            raise ValueError("customer_phone must be a valid mobile number (10 to 15 digits)")
        return cleaned


class TokenOut(BaseModel):
    id: str
    service_id: str
    date: date
    token_number: int
    status: TokenStatus
    is_walk_in: bool
    customer_name: Optional[str] = None
    booking_time: datetime

    class Config:
        from_attributes = True


class BookingSuccessOut(BaseModel):
    organization_name: str
    service_name: str
    token_number: int
    current_token: Optional[int] = None
    customers_before_you: int
    estimated_waiting_time_minutes: int
    estimated_arrival_time: Optional[datetime] = None
    status: BookingStatus


class BookingHistoryOut(BaseModel):
    booking_id: str
    organization_name: str
    service_name: str
    token_number: int
    status: BookingStatus
    booking_time: datetime
    service_id: Optional[str] = None

    class Config:
        from_attributes = True


# ---------- Notifications ----------

class NotificationOut(BaseModel):
    id: str
    message: str
    read_status: bool
    created_at: datetime

    class Config:
        from_attributes = True


# ---------- Organization dashboard ----------

class QueueTokenOut(BaseModel):
    token_id: str
    token_number: int
    status: TokenStatus
    customer_name: Optional[str] = None
    is_walk_in: bool

    class Config:
        from_attributes = True


class DashboardStatsOut(BaseModel):
    todays_bookings: int
    current_token: Optional[int] = None
    completed_tokens: int
    pending_tokens: int
    cancelled_tokens: int
    average_waiting_time_minutes: int


class ReportsOut(BaseModel):
    todays_bookings: int
    completed_tokens: int
    cancelled_tokens: int
    average_waiting_time_minutes: int
    most_booked_service: Optional[str] = None
    peak_hour: Optional[str] = None

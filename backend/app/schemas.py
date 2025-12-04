from pydantic import BaseModel, EmailStr
from typing import Optional
from uuid import UUID

# ---------------- User Schemas ----------------
class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str
    phone_number: Optional[str] = None

class UserUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None
    phone_number: Optional[str] = None

class UserResponse(BaseModel):
    id: UUID
    name: str
    email: EmailStr
    phone_number: Optional[str] = None

    class Config:
        orm_mode = True
        from_attributes = True


# ---------------- Driver Schemas ----------------
class DriverCreate(BaseModel):
    name: str
    phone: str
    stand_id: int
    is_available: bool = False
    password: str

class DriverUpdate(BaseModel):
    name: Optional[str] = None
    phone: Optional[str] = None
    stand_id: Optional[int] = None
    is_available: Optional[bool] = None


# ---------------- Ride Schemas ----------------
from datetime import datetime

class RideCreate(BaseModel):
    user_id: int
    start_location: str
    end_location: str

class RideUpdate(BaseModel):
    driver_id: Optional[int] = None
    status: Optional[str] = None  # pending, accepted, completed, cancelled

class RideResponse(BaseModel):
    id: int
    user_id: int
    driver_id: Optional[int]
    start_location: str
    end_location: str
    status: str
    requested_at: datetime

    class Config:
        orm_mode = True


# ---------------- AutoStand Schemas ----------------
class AutoStandCreate(BaseModel):
    name: str
    location: str

class AutoStandUpdate(BaseModel):
    name: Optional[str] = None
    location: Optional[str] = None

class AutoStandResponse(BaseModel):
    id: int
    name: str
    location: str

    class Config:
        orm_mode = True


# -----------------Token / Auth schemas-------------
class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

class TokenData(BaseModel):
    sub: Optional[str] = None
    role: Optional[str] = None

# Login schema for drivers (if you want JSON login)
class DriverLogin(BaseModel):
    phone: str
    password: str


# -----------------Payloads-------------
class AvailabilityPayload(BaseModel):
    available: bool

class LocationPayload(BaseModel):
    lat: float
    lng: float
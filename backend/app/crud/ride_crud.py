from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.model import Ride, User, Driver
from app.schemas import RideCreate, RideUpdate
from datetime import datetime

# ---------------- Create Ride ----------------
def create_ride(db: Session, ride: RideCreate):
    # Optional: check if user exists
    user = db.query(User).filter(User.id == ride.user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    new_ride = Ride(
        user_id=ride.user_id,
        start_location=ride.start_location,
        end_location=ride.end_location,
        status="pending",
        requested_at=datetime.utcnow()
    )
    db.add(new_ride)
    db.commit()
    db.refresh(new_ride)
    return new_ride

# ---------------- Get Ride by ID ----------------
def get_ride_by_id(db: Session, ride_id: int):
    ride = db.query(Ride).filter(Ride.id == ride_id).first()
    if not ride:
        raise HTTPException(status_code=404, detail="Ride not found")
    return ride

# ---------------- Update Ride ----------------
def update_ride(db: Session, ride_id: int, ride_data: RideUpdate):
    ride = get_ride_by_id(db, ride_id)
    for key, value in ride_data.dict(exclude_unset=True).items():
        setattr(ride, key, value)
    db.commit()
    db.refresh(ride)
    return ride

# ---------------- List Rides ----------------
def get_rides(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Ride).offset(skip).limit(limit).all()

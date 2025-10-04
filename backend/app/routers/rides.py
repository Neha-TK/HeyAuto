from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.crud import ride_crud
from app.schemas import RideCreate, RideUpdate, RideResponse

router = APIRouter()

# ---------------- Create Ride ----------------
@router.post("/", response_model=RideResponse)
def create_ride(ride: RideCreate, db: Session = Depends(get_db)):
    return ride_crud.create_ride(db, ride)

# ---------------- Get Ride ----------------
@router.get("/{ride_id}", response_model=RideResponse)
def get_ride(ride_id: int, db: Session = Depends(get_db)):
    return ride_crud.get_ride_by_id(db, ride_id)

# ---------------- Update Ride ----------------
@router.put("/{ride_id}", response_model=RideResponse)
def update_ride(ride_id: int, ride_data: RideUpdate, db: Session = Depends(get_db)):
    return ride_crud.update_ride(db, ride_id, ride_data)

# ---------------- List Rides ----------------
@router.get("/", response_model=list[RideResponse])
def list_rides(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return ride_crud.get_rides(db, skip, limit)

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.crud import driver_crud
from app.schemas import DriverCreate, DriverUpdate
from app.database import get_db
from app.utils.auth import get_current_driver

router = APIRouter(prefix="/drivers", tags=["Drivers"])

# ---------------- Create ----------------
@router.post("/", response_model=dict)
def create_driver_endpoint(driver: DriverCreate, db: Session = Depends(get_db)):
    new_driver = driver_crud.create_driver(db, driver)
    return {"status": "success", "driver": {"id": new_driver.id, "name": new_driver.name, "phone": new_driver.phone, "stand_id": new_driver.stand_id, "is_available": new_driver.is_available}}


# ---------------- Read ----------------
@router.get("/{driver_id}", response_model=dict)
def get_driver_by_id_endpoint(driver_id: int, db: Session = Depends(get_db)):
    driver = driver_crud.get_driver_by_id(db, driver_id)
    if not driver:
        raise HTTPException(status_code=404, detail="Driver not found")
    return {"id": driver.id, "name": driver.name, "phone": driver.phone, "stand_id": driver.stand_id, "is_available": driver.is_available}


@router.get("/", response_model=List[dict])
def get_drivers_endpoint(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    drivers = driver_crud.get_drivers(db, skip, limit)
    return [{"id": d.id, "name": d.name, "phone": d.phone, "stand_id": d.stand_id, "is_available": d.is_available} for d in drivers]


@router.get("/by-phone/", response_model=dict)
def get_driver_by_phone_endpoint(phone: str, db: Session = Depends(get_db)):
    driver = driver_crud.get_driver_by_phone(db, phone)
    if not driver:
        raise HTTPException(status_code=404, detail="Driver not found")
    return {"id": driver.id, "name": driver.name, "phone": driver.phone, "stand_id": driver.stand_id, "is_available": driver.is_available}


# ---------------- Update ----------------
@router.put("/{driver_id}", response_model=dict)
def update_driver_endpoint(driver_id: int, driver_data: DriverUpdate, current_driver = Depends(get_current_driver), db: Session = Depends(get_db)):
    if current_driver.id != driver_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not allowed")
    updated_driver = driver_crud.update_driver(db, driver_id, driver_data)
    return {"status": "success", "driver": {"id": updated_driver.id, "name": updated_driver.name, "phone": updated_driver.phone, "stand_id": updated_driver.stand_id, "is_available": updated_driver.is_available}}


# ---------------- Delete ----------------
@router.delete("/{driver_id}", response_model=dict)
def delete_driver_endpoint(driver_id: int, current_driver = Depends(get_current_driver), db: Session = Depends(get_db)):
    if current_driver.id != driver_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not allowed")
    return driver_crud.delete_driver(db, driver_id)


# ---------------- Testing endpoint ----------------
@router.get("/me", response_model=dict)
def read_current_driver(current_driver = Depends(get_current_driver)):
    return {"id": current_driver.id, "name": current_driver.name, "phone": current_driver.phone, "stand_id": current_driver.stand_id}


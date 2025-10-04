from sqlalchemy.orm import Session
from app.model import Driver
from app.schemas import DriverCreate, DriverUpdate
from fastapi import HTTPException

# ---------------- Create ----------------
def create_driver(db: Session, driver_data: DriverCreate):
    # Check if phone exists
    existing_driver = db.query(Driver).filter(Driver.phone == driver_data.phone).first()
    if existing_driver:
        raise HTTPException(status_code=400, detail="Phone already registered")

    new_driver = Driver(
        name=driver_data.name,
        phone=driver_data.phone,
        stand_id=driver_data.stand_id,
        is_available=driver_data.is_available
    )

    db.add(new_driver)
    db.commit()
    db.refresh(new_driver)
    return new_driver


# ---------------- Read ----------------
def get_driver_by_id(db: Session, driver_id: int):
    return db.query(Driver).filter(Driver.id == driver_id).first()


def get_driver_by_phone(db: Session, phone: str):
    return db.query(Driver).filter(Driver.phone == phone).first()


def get_drivers(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Driver).offset(skip).limit(limit).all()


# ---------------- Update ----------------
def update_driver(db: Session, driver_id: int, driver_data: DriverUpdate):
    driver = get_driver_by_id(db, driver_id)
    if not driver:
        raise HTTPException(status_code=404, detail="Driver not found")

    driver.name = driver_data.name or driver.name
    driver.phone = driver_data.phone or driver.phone
    driver.stand_id = driver_data.stand_id or driver.stand_id
    if driver_data.is_available is not None:
        driver.is_available = driver_data.is_available

    db.commit()
    db.refresh(driver)
    return driver


# ---------------- Delete ----------------
def delete_driver(db: Session, driver_id: int):
    driver = get_driver_by_id(db, driver_id)
    if not driver:
        raise HTTPException(status_code=404, detail="Driver not found")

    db.delete(driver)
    db.commit()
    return {"status": "success", "message": f"Driver {driver_id} deleted"}

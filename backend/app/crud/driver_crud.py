from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from app.model import Driver
from app.schemas import DriverCreate, DriverUpdate
from app.utils.security import hash_password

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
        is_available=driver_data.is_available,
        password=hash_password(driver_data.password)
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


# # ---------------- Mark Presence ----------------
# def mark_presence(db: Session, driver_id: int) -> Driver:
#     """
#     Mark driver as present at their stand.
#     Current behaviour (simple):
#       - ensures driver exists
#       - sets is_available = False (present but not actively accepting rides)
#     Later: add an `is_present` boolean + timestamp and optionally add to a stand queue.
#     """
#     driver = db.query(Driver).filter(Driver.id == driver_id).first()
#     if not driver:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Driver not found")

#     # simple behavior: mark them present by ensuring they are not available by default
#     driver.is_available = False

#     db.add(driver)
#     db.commit()
#     db.refresh(driver)
#     return driver


# ---------------- Set availability ----------------
def set_availability(db: Session, driver_id: int, available: bool) -> Driver:
    driver = db.query(Driver).filter(Driver.id == driver_id).first()
    if not driver:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Driver not found")

    driver.is_available = bool(available)
    db.add(driver)
    db.commit()
    db.refresh(driver)
    return driver


# ---------------- Update location ----------------
def update_location(db: Session, driver_id: int, lat: float, lng: float) -> Driver:
    """
    Currently not implemented because  Driver model doesn't have latitude/longitude columns.

    """
    raise HTTPException(status_code=status.HTTP_501_NOT_IMPLEMENTED,
                        detail="Location tracking not implemented. Add latitude/longitude to Driver model and DB migration first.")

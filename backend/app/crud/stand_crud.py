from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from datetime import datetime
from app.model import AutoStand, Driver, StandQueue
from app.schemas import AutoStandCreate, AutoStandUpdate

# ---------------- Create Stand ----------------
def create_stand(db: Session, stand: AutoStandCreate):
    new_stand = AutoStand(name=stand.name, location=stand.location)
    db.add(new_stand)
    db.commit()
    db.refresh(new_stand)
    return new_stand

# ---------------- Get Stand ----------------
def get_stand(db: Session, stand_id: int):
    stand = db.query(AutoStand).filter(AutoStand.id == stand_id).first()
    if not stand:
        raise HTTPException(status_code=404, detail="AutoStand not found")
    return stand

# ---------------- Update Stand ----------------
def update_stand(db: Session, stand_id: int, stand_data: AutoStandUpdate):
    stand = get_stand(db, stand_id)
    for key, value in stand_data.dict(exclude_unset=True).items():
        setattr(stand, key, value)
    db.commit()
    db.refresh(stand)
    return stand

# ---------------- List Stands ----------------
def get_stands(db: Session, skip: int = 0, limit: int = 100):
    return db.query(AutoStand).offset(skip).limit(limit).all()

# ---------------- Add Driver to Queue ----------------
def add_driver_to_queue(db: Session, stand_id: int, driver_id: int) -> StandQueue:
    # ensure stand exists
    stand = db.query(AutoStand).filter(AutoStand.id == stand_id).first()
    if not stand:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Stand not found")

    # ensure driver exists
    driver = db.query(Driver).filter(Driver.id == driver_id).first()
    if not driver:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Driver not found")
    
    # ensure driver belongs to this stand
    if driver.stand_id != stand_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Driver does not belong to this stand"
        )
    
    # check if already in queue and still waiting
    existing = db.query(StandQueue).filter(StandQueue.driver_id == driver_id, StandQueue.status == "waiting").first()
    if existing:
        return existing
    
    entry = StandQueue(
        stand_id=stand_id,
        driver_id=driver_id,
        joined_at=datetime.utcnow(),
        status="waiting"
    )

    db.add(entry)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Could not join queue")
    db.refresh(entry)
    return entry
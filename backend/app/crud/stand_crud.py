from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.model import AutoStand
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

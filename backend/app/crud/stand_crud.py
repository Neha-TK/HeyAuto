from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
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

# ---------------- Remove Driver from Queue ----------------
def remove_driver_from_queue(db: Session, driver_id: int) -> None:
    entry = db.query(StandQueue).filter(StandQueue.driver_id == driver_id, StandQueue.status == "waiting").first()
    if not entry:
        return None
    entry.status = "left"
    db.add(entry)
    db.commit()
    db.refresh(entry)
    return entry

# ---------------- Get Queue ----------------
def get_queue(db: Session, stand_id: int):
    entries = (db.query(StandQueue)
                 .filter(StandQueue.stand_id == stand_id, StandQueue.status == "waiting")
                 .order_by(StandQueue.joined_at.asc())
                 .all())
    return entries

# ---------------- Pop Driver ----------------
def pop_next_driver(db: Session, stand_id: int):
    """
    Transaction-safe pop: selects the oldest waiting StandQueue row for the given stand,
    locks it (FOR UPDATE SKIP LOCKED), marks it as 'assigned' and returns the entry.

    Returns None if no waiting driver exists.
    """

    # ensure stand exist
    stand = db.query(AutoStand).filter(AutoStand.id == stand_id).first()
    if not stand:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Stand not found")

    try:
        # Use a transaction context so the SELECT FOR UPDATE and update happen atomically.
        with db.begin():
            stmt = (
                select(StandQueue)
                .where(StandQueue.stand_id == stand_id, StandQueue.status == "waiting")
                .order_by(StandQueue.joined_at.asc())
                .with_for_update(skip_locked=True)
                .limit(1)
            )
            result = db.execute(stmt).scalars().first()

            if not result:
                # no waiting drivers (or all waiting rows locked by other transactions)
                return None

            # mark as assigned within the same transaction
            result.status = "assigned"
            result.assigned_at = datetime.utcnow()
            db.add(result)
            # leaving the with db.begin() block will commit --> When the with block ends: If there is NO error → SQLAlchemy runs COMMIT, If there IS an error → SQLAlchemy runs ROLLBACK automatically
      
        db.refresh(result)
        return result

    except SQLAlchemyError as exc:
        # Rollback handled by the context manager, but we still raise an HTTP error
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail="Database error when popping next driver") from exc

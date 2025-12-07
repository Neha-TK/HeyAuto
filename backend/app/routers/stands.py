from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.crud import stand_crud
from app.schemas import AutoStandCreate, AutoStandUpdate, AutoStandResponse
from app.utils.auth import get_current_driver

router = APIRouter()

# ---------------- Create Stand ----------------
@router.post("/", response_model=AutoStandResponse)
def create_stand(stand: AutoStandCreate, db: Session = Depends(get_db)):
    return stand_crud.create_stand(db, stand)

# ---------------- Get Stand ----------------
@router.get("/{stand_id}", response_model=AutoStandResponse)
def get_stand(stand_id: int, db: Session = Depends(get_db)):
    return stand_crud.get_stand(db, stand_id)

# ---------------- Update Stand ----------------
@router.put("/{stand_id}", response_model=AutoStandResponse)
def update_stand(stand_id: int, stand_data: AutoStandUpdate, db: Session = Depends(get_db)):
    return stand_crud.update_stand(db, stand_id, stand_data)

# ---------------- List Stands ----------------
@router.get("/", response_model=list[AutoStandResponse])
def list_stands(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return stand_crud.get_stands(db, skip, limit)

# ---------------- Add Driver to Queue ----------------
@router.post("/{stand_id}/join", response_model=dict)
def join_queue(stand_id: int, current_driver = Depends(get_current_driver), db: Session = Depends(get_db)):
    entry = stand_crud.add_driver_to_queue(db, stand_id, current_driver.id)
    return {"status": "success", "queue_id": entry.id, "driver_id": entry.driver_id, "joined_at": entry.joined_at.isoformat()}

# ---------------- Remove Driver from Queue ----------------
@router.post("/me/leave", response_model=dict)
def leave_queue(current_driver = Depends(get_current_driver), db: Session = Depends(get_db)):
    entry = stand_crud.remove_driver_from_queue(db, current_driver.id)
    if not entry:
        raise HTTPException(status_code=404, detail="You are not in a queue")
    return {"status": "success", "driver_id": entry.driver_id}

# ---------------- Get Queue ----------------
@router.get("/{stand_id}/queue", response_model=list)
def get_queue(stand_id: int, db: Session = Depends(get_db)):
    entries = stand_crud.get_queue(db, stand_id)
    # return a simple list of driver ids and joined_at
    return [{"id": e.id, "driver_id": e.driver_id, "joined_at": e.joined_at.isoformat()} for e in entries]

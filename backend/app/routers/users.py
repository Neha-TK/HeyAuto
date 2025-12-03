from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.crud import user_crud
from app.schemas import UserCreate, UserUpdate
from app.database import get_db
from app.utils.auth import get_current_user

router = APIRouter(tags=["Users"])

# ---------------- Create ----------------
@router.post("/", response_model=dict)
def create_user_endpoint(user: UserCreate, db: Session = Depends(get_db)):
    new_user = user_crud.create_user(db, user)
    return {"status": "success", "user": {"id": new_user.id, "name": new_user.name, "email": new_user.email}}


# ---------------- Read ----------------
@router.get("/{user_id}", response_model=dict)
def get_user_by_id_endpoint(user_id: int, db: Session = Depends(get_db)):
    user = user_crud.get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return {"id": user.id, "name": user.name, "email": user.email}


@router.get("/", response_model=List[dict])
def get_users_endpoint(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = user_crud.get_users(db, skip, limit)
    return [{"id": u.id, "name": u.name, "email": u.email} for u in users]


@router.get("/by-email/", response_model=dict)
def get_user_by_email_endpoint(email: str, db: Session = Depends(get_db)):
    user = user_crud.get_user_by_email(db, email)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return {"id": user.id, "name": user.name, "email": user.email}


# ---------------- Update ----------------
@router.put("/{user_id}", response_model=dict)
def update_user_endpoint(user_id: int, user_data: UserUpdate, current_user = Depends(get_current_user), db: Session = Depends(get_db)):
    if current_user.id != user_id:
        raise HTTPException(status_code=403, detail="Not allowed")
    updated_user = user_crud.update_user(db, user_id, user_data)
    return {"status": "success", "user": {"id": updated_user.id, "name": updated_user.name, "email": updated_user.email}}


# ---------------- Delete ----------------
@router.delete("/{user_id}", response_model=dict)
def delete_user_endpoint(user_id: int, db: Session = Depends(get_db)):
    return user_crud.delete_user(db, user_id)


# ---------------- Test endpoints ----------------
@router.get("/me", response_model=dict)
def read_current_user(current_user = Depends(get_current_user)):
    return {"id": current_user.id, "name": current_user.name, "email": current_user.email}

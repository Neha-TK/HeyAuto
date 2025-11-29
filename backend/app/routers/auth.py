from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas import Token, DriverLogin
from app.utils.auth import create_access_token, authenticate_user_by_email, authenticate_driver_by_phone
from app.config import settings

router = APIRouter(tags=["Auth"])

# ---------- User login (OAuth2 form) ----------
# This endpoint accepts form data: username and password
# username will be the user's email
@router.post("/token", response_model=Token)
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = authenticate_user_by_email(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect email or password")
    access_token = create_access_token({"sub": str(user.id), "role": "user"})
    return {"access_token": access_token, "token_type": "bearer"}


# ---------- Driver login (JSON) ----------
@router.post("/driver/token", response_model=Token)
def driver_login(login: DriverLogin, db: Session = Depends(get_db)):
    driver = authenticate_driver_by_phone(db, login.phone, login.password)
    if not driver:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect phone or password")
    access_token = create_access_token({"sub": str(driver.id), "role": "driver"})
    return {"access_token": access_token, "token_type": "bearer"}

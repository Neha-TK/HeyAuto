from datetime import datetime, timedelta
from typing import Optional

from jose import jwt, JWTError
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app.database import get_db
from app import model
from app.schemas import TokenData
from app.config import settings
from app.utils.security import verify_password

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta if expires_delta else timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)
    return encoded_jwt

def decode_access_token(token: str) -> dict:
    try:
        payload = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
        return payload
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

# Dependency to get current user (role = "user")
def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    payload = decode_access_token(token)
    sub = payload.get("sub")
    role = payload.get("role")
    if sub is None or role != "user":
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid authentication credentials")
    user = db.query(model.User).filter(model.User.id == int(sub)).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")
    return user

# Dependency to get current driver (role = "driver")
def get_current_driver(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    payload = decode_access_token(token)
    sub = payload.get("sub")
    role = payload.get("role")
    if sub is None or role != "driver":
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid authentication credentials")
    driver = db.query(model.Driver).filter(model.Driver.id == int(sub)).first()
    if not driver:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Driver not found")
    return driver

# Utility to authenticate with email/password for user
def authenticate_user_by_email(db: Session, email: str, password: str):
    user = db.query(model.User).filter(model.User.email == email).first()
    if not user:
        return None
    if not verify_password(password, user.password):
        return None
    return user

# Utility to authenticate driver by phone/password
def authenticate_driver_by_phone(db: Session, phone: str, password: str):
    driver = db.query(model.Driver).filter(model.Driver.phone == phone).first()
    if not driver:
        return None
    if not verify_password(password, driver.password):
        return None
    return driver

from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base

# ---------------- User ----------------
class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True)
    password = Column(String, nullable=False)  
    created_at = Column(DateTime, default=datetime.utcnow)
    
    rides = relationship("Ride", back_populates="user")


# ---------------- Driver ----------------
class Driver(Base):
    __tablename__ = "drivers"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    phone = Column(String, unique=True)
    is_available = Column(Boolean, default=False)
    stand_id = Column(Integer, ForeignKey("autostands.id"))
    created_at = Column(DateTime, default=datetime.utcnow)
    
    stand = relationship("AutoStand", back_populates="drivers")
    rides = relationship("Ride", back_populates="driver")


# ---------------- AutoStand ----------------
class AutoStand(Base):
    __tablename__ = "autostands"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    location = Column(String, nullable=False)
    
    drivers = relationship("Driver", back_populates="stand")


# ---------------- Ride ----------------
class Ride(Base):
    __tablename__ = "rides"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    driver_id = Column(Integer, ForeignKey("drivers.id"), nullable=True) # nullable=True → a ride may exist before a driver is assigned.
    start_location = Column(String, nullable=False)
    end_location = Column(String, nullable=False)
    status = Column(String, default="pending")  # pending, accepted, completed, cancelled
    requested_at = Column(DateTime, default=datetime.utcnow)
    
    user = relationship("User", back_populates="rides")
    driver = relationship("Driver", back_populates="rides")

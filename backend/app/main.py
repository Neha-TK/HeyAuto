from fastapi import FastAPI
from app.config import settings
from app.database import Base, engine
from app.routers import users, drivers, rides, stands
from app import model


# Create tables
Base.metadata.create_all(bind=engine)

# FastAPI app instance
app = FastAPI(title=settings.PROJECT_NAME)

# Include routers
app.include_router(users.router, prefix="/users", tags=["Users"])
app.include_router(drivers.router, prefix="/drivers", tags=["Drivers"])
app.include_router(rides.router, prefix="/rides", tags=["Rides"])
app.include_router(stands.router, prefix="/stands", tags=["AutoStands"])


@app.get("/")
def test():
    return {"status": "ok", "message": "Backend is running"}

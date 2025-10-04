from fastapi import FastAPI
from app.config import settings
from app.database import Base, engine

from app import model


# Create tables
Base.metadata.create_all(bind=engine)

# FastAPI app instance
app = FastAPI(title=settings.PROJECT_NAME)

@app.get("/")
def test():
    return {"status": "ok", "message": "Backend is running 🚀"}

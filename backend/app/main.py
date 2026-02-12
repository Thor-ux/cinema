from fastapi import FastAPI
from app.database import Base, engine
from app.api import admin
from pydantic_settings import BaseSettings


Base.metadata.create_all(bind=engine)

app = FastAPI(title="Cinema Booking")

@app.get("/")
def root():
    return {"status": "Cinema API"}

app.include_router(admin.router, prefix="/admin", tags=["Admin"])
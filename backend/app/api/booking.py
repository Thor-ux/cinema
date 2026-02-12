from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.core.security import get_current_user
from app.services.booking import reserve_seat

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/reserve")
def reserve(showtime_id: int, seat_id: int,
            user_id: int = Depends(get_current_user),
            db: Session = Depends(get_db)):
    return reserve_seat(db, showtime_id, seat_id, user_id)

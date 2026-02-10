from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.services.booking import reserve_seat

router = APIRouter(prefix="/booking", tags=["Booking"])


# DB dependency (FastAPI standard)
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/reserve")
def reserve(
    showtime_id: int,
    seat_id: int,
    db: Session = Depends(get_db),
):
    result = reserve_seat(db, showtime_id, seat_id)

    if not result:
        raise HTTPException(
            status_code=400,
            detail="Seat is already reserved or unavailable"
        )

    return {
        "status": "HELD",
        "showtime_id": showtime_id,
        "seat_id": seat_id
    }

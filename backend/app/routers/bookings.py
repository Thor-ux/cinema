from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.dependencies.db import get_db
from app.schemas.booking import BookingCreate
from app.services.booking import create_booking

router = APIRouter(tags=["Bookings"])


@router.post("/bookings")
def book_seats(data: BookingCreate, db: Session = Depends(get_db)):

    tickets = create_booking(db, data)

    return tickets
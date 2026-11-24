from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.dependencies.auth import get_current_user
from app.dependencies.db import get_db
from app.models import Booking, User
from app.schemas.booking import BookingCreate, BookingRead
from app.services.booking import booking_to_read, create_booking

router = APIRouter(prefix="/bookings", tags=["Bookings"])


@router.post("", response_model=BookingRead, status_code=status.HTTP_201_CREATED)
def book_seats(data: BookingCreate, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    return booking_to_read(create_booking(db, data, user))


@router.get("/me", response_model=list[BookingRead])
def my_bookings(db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    bookings = db.query(Booking).filter(Booking.user_id == user.id).order_by(Booking.id.desc()).all()
    return [booking_to_read(b) for b in bookings]

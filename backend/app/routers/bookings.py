from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import select
from app import models, schemas
from app.dependencies import get_db

router = APIRouter(prefix="/bookings", tags=["Bookings"])


@router.post("/", response_model=schemas.Booking)
def create_booking(data: schemas.BookingCreate, db: Session = Depends(get_db)):

    screening = db.query(models.Screening).filter(
        models.Screening.id == data.screening_id
    ).first()

    if not screening:
        raise HTTPException(status_code=404, detail="Screening not found")

    # Lock seats to prevent double booking
    seats = (
        db.query(models.Seat)
        .filter(
            models.Seat.id.in_(data.seat_ids),
            models.Seat.screening_id == data.screening_id,
            models.Seat.is_reserved == False,
        )
        .with_for_update()
        .all()
    )

    if len(seats) != len(data.seat_ids):
        raise HTTPException(status_code=400, detail="Some seats already reserved")

    booking = models.Booking(
        customer_name=data.customer_name,
        screening_id=data.screening_id,
    )

    db.add(booking)
    db.flush()  # Get booking ID

    for seat in seats:
        seat.is_reserved = True
        seat.booking_id = booking.id

    db.commit()
    db.refresh(booking)

    return booking
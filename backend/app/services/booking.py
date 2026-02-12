from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException
from app.models.booking import Booking

def reserve_seat(db, showtime_id, seat_id, user_id):
    booking = Booking(
        user_id=user_id,
        showtime_id=showtime_id,
        seat_id=seat_id,
    )

    try:
        db.add(booking)
        db.commit()
        db.refresh(booking)
        return booking
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Seat already booked")

import uuid
from fastapi import HTTPException
from sqlalchemy import and_

from app.models.booking import Booking
from app.models.ticket import Ticket
from app.models.seat import Seat
from app.models.session import Session
from app.utils.qr import generate_qr


def create_booking(db, data):

    seats = (
        db.query(Seat)
        .filter(Seat.id.in_(data.seat_ids))
        .with_for_update()
        .all()
    )

    if len(seats) != len(data.seat_ids):
        raise HTTPException(status_code=404, detail="Some seats not found")
    
    existing = (
        db.query(Ticket.seat_id)
        .join(Booking)
        .filter(
            Booking.session_id == data.session_id,
            Ticket.seat_id.in_(data.seat_ids)
        )
        .all()
    )

    if existing:
        raise HTTPException(status_code=400, detail="Some seats already booked")

    booking_code = str(uuid.uuid4())[:8]

    booking = Booking(
        session_id=data.session_id,
        customer_name=data.customer_name,
        booking_code=booking_code
    )

    db.add(booking)
    db.flush()

    tickets = []

    for seat in seats:
        qr_content = {
    "booking_code": booking_code,
    "session_id": data.session_id,
    "movie_id": Session.movie_id,
    "seat": {
        "row": seat.row,
        "number": seat.number,
        "type": seat.type
    },
}

        qr = generate_qr(qr_content)

        ticket = Ticket(
            booking_id=booking.id,
            seat_id=seat.id,
            qr_code=qr
        )

        db.add(ticket)
        tickets.append(ticket)

    db.commit()

    return tickets
import secrets

from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session as DbSession

from app.core.config import settings
from app.models import Booking, Seat, Session, Ticket, User
from app.schemas.booking import BookingCreate, BookingRead, TicketRead
from app.utils.qr import generate_qr


def seat_price(session: Session, seat: Seat) -> float:
    multiplier = settings.VIP_PRICE_MULTIPLIER if seat.type == "vip" else 1.0
    return round(session.price * multiplier, 2)


def create_booking(db: DbSession, data: BookingCreate, user: User) -> Booking:
    session = db.get(Session, data.session_id)
    if session is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Session not found")
    if not session.hall.is_active:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "This hall is closed")

    seat_ids = set(data.seat_ids)
    if len(seat_ids) != len(data.seat_ids):
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "The same seat was selected twice")

    seats = db.query(Seat).filter(Seat.id.in_(seat_ids), Seat.hall_id == session.hall_id).all()
    if len(seats) != len(seat_ids):
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "Some seats do not exist in this hall")

    taken = (
        db.query(Ticket.seat_id)
        .filter(Ticket.session_id == session.id, Ticket.seat_id.in_(seat_ids))
        .first()
    )
    if taken:
        raise HTTPException(status.HTTP_409_CONFLICT, "Some seats are already booked")

    booking = Booking(
        session_id=session.id,
        user_id=user.id,
        customer_name=data.customer_name.strip(),
        booking_code=secrets.token_hex(4).upper(),
    )
    db.add(booking)
    db.flush()

    for seat in sorted(seats, key=lambda s: (s.row, s.number)):
        qr_text = "\n".join([
            f"BOOKING:{booking.booking_code}",
            f"MOVIE:{session.movie.title}",
            f"SESSION:{session.id}",
            f"START:{session.start_time.isoformat()}",
            f"HALL:{session.hall.name}",
            f"ROW:{seat.row}",
            f"SEAT:{seat.number}",
            f"TYPE:{seat.type}",
        ])
        db.add(Ticket(
            booking_id=booking.id,
            session_id=session.id,
            seat_id=seat.id,
            price=seat_price(session, seat),
            qr_code=generate_qr(qr_text),
        ))

    try:
        db.commit()
    except IntegrityError:
        # Another request booked one of these seats between our check and commit.
        db.rollback()
        raise HTTPException(status.HTTP_409_CONFLICT, "Some seats are already booked")

    db.refresh(booking)
    return booking


def booking_to_read(booking: Booking) -> BookingRead:
    session = booking.session
    return BookingRead(
        id=booking.id,
        booking_code=booking.booking_code,
        customer_name=booking.customer_name,
        session_id=session.id,
        movie_title=session.movie.title,
        start_time=session.start_time,
        hall_name=session.hall.name,
        total_price=booking.total_price,
        tickets=[
            TicketRead(
                id=t.id,
                seat_id=t.seat_id,
                row=t.seat.row,
                number=t.seat.number,
                seat_type=t.seat.type,
                price=t.price,
                qr_code=t.qr_code,
            )
            for t in sorted(booking.tickets, key=lambda t: (t.seat.row, t.seat.number))
        ],
    )

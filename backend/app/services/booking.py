from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from app.models.ticket import Ticket


RESERVATION_MINUTES = 10


def reserve_seat(db: Session, showtime_id: int, seat_id: int):
    # Check if seat already booked or held
    existing = db.query(Ticket).filter(
        Ticket.showtime_id == showtime_id,
        Ticket.seat_id == seat_id,
        Ticket.status.in_(["HELD", "BOOKED"])
    ).first()

    if existing:
        return None

    ticket = Ticket(
        showtime_id=showtime_id,
        seat_id=seat_id,
        status="HELD",
        expires_at=datetime.utcnow() + timedelta(minutes=RESERVATION_MINUTES)
    )

    db.add(ticket)
    db.commit()
    db.refresh(ticket)

    return ticket

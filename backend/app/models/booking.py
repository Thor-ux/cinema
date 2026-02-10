from datetime import datetime, timedelta

def hold_seat(db, seat_id, showtime_id):
    expires = datetime.utcnow() + timedelta(minutes=10)

    ticket = Ticket(
        seat_id=seat_id,
        showtime_id=showtime_id,
        status="HELD",
        expires_at=expires
    )
    db.add(ticket)
    db.commit()

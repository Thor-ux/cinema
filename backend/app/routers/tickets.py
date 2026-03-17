from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import text

from app.dependencies.db import get_db
from app.dependencies.auth import get_current_user

router = APIRouter(tags=["Tickets"])

@router.get("/me")
def my_tickets(db: Session = Depends(get_db), user=Depends(get_current_user)):
    query = text("""
        SELECT
            tickets.id,
            tickets.qr_code,
            seats.number AS seat_number,
            sessions.start_time,
            movies.title AS movie_title
        FROM tickets
        JOIN seats ON tickets.seat_id = seats.id
        JOIN bookings ON bookings.id = tickets.booking_id
        JOIN sessions ON bookings.session_id = sessions.id
        JOIN movies ON sessions.movie_id = movies.id
        WHERE bookings.user_id = :user_id
    """)
    result = db.execute(query, {"user_id": user.id})

    tickets = []
    for row in result:
        tickets.append({
            "id": row.id,
            "qr_code": row.qr_code,
            "seat_number": row.seat_number,
            "start_time": row.start_time,
            "movie_title": row.movie_title
        })
    return tickets
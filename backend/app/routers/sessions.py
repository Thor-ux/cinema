from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.dependencies.db import get_db
from app.dependencies.auth import get_current_admin
from app.models.session import Session as MovieSession
from app.models.seat import Seat
from app.models.hall import CinemaHall
from app.schemas.session import SessionCreate
from app.models.ticket import Ticket
from app.models.booking import Booking

router = APIRouter(tags=["Sessions"])

@router.get("/movies/{movie_id}/showtimes")
def get_showtimes(movie_id: int, db: Session = Depends(get_db)):

    showtimes = (
        db.query(MovieSession)
        .filter(MovieSession.movie_id == movie_id)
        .all()
    )

    return showtimes

@router.get("/sessions/{session_id}/seats")
def get_session_seats(session_id: int, db: Session = Depends(get_db)):

    session = db.query(MovieSession).filter(
        MovieSession.id == session_id
    ).first()

    if not session:
        raise HTTPException(404, "Session not found")

    seats = db.query(Seat).filter(
        Seat.hall_id == session.hall_id
    ).all()

    booked = (
        db.query(Ticket.seat_id)
        .join(Booking)
        .filter(Booking.session_id == session_id)
        .all()
    )

    booked_ids = [s[0] for s in booked]

    return [
        {
            "id": seat.id,
            "row": seat.row,
            "number": seat.number,
            "is_reserved": seat.id in booked_ids
        }
        for seat in seats
    ]

@router.post("/admin/sessions")
def create_session(data: SessionCreate, db: Session = Depends(get_db), admin=Depends(get_current_admin)):

    hall = db.query(CinemaHall).filter(
        CinemaHall.id == data.hall_id
    ).first()

    if not hall:
        raise HTTPException(404, "Hall not found")

    session = MovieSession(**data.dict())

    db.add(session)
    db.commit()
    db.refresh(session)

    for r in range(1, hall.rows + 1):
        for s in range(1, hall.seats_per_row + 1):

            seat = Seat(
                hall_id=hall.id,
                session_id=session.id,
                row=r,
                number=s
            )

            db.add(seat)

    db.commit()

    return session

@router.get("/admin/sessions")
def get_sessions(db: Session = Depends(get_db), admin=Depends(get_current_admin)):

    return db.query(MovieSession).all()

@router.put("/admin/sessions/{session_id}")
def update_session(session_id: int, data: SessionCreate, db: Session = Depends(get_db), admin=Depends(get_current_admin)):

    session = db.query(MovieSession).filter(
        MovieSession.id == session_id
    ).first()

    if not session:
        raise HTTPException(404, "Session not found")

    for key, value in data.dict().items():
        setattr(session, key, value)

    db.commit()

    return session

@router.delete("/admin/sessions/{session_id}")
def delete_session(session_id: int, db: Session = Depends(get_db), admin=Depends(get_current_admin)):

    session = db.query(MovieSession).filter(
        MovieSession.id == session_id
    ).first()

    if not session:
        raise HTTPException(404, "Session not found")

    db.delete(session)
    db.commit()

    return {"message": "Session deleted"}
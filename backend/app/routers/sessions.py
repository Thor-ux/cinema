from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.dependencies.auth import get_current_admin
from app.dependencies.db import get_db
from app.models import Booking, CinemaHall, Movie, Seat, Ticket
from app.models import Session as MovieSession
from app.schemas.session import SeatStatus, SessionCreate, SessionRead

router = APIRouter(tags=["Sessions"])


def _get_session(db: Session, session_id: int) -> MovieSession:
    session = db.get(MovieSession, session_id)
    if session is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Session not found")
    return session


def _naive(dt):
    # SQLite returns naive datetimes; compare everything as naive UTC-agnostic values.
    return dt.replace(tzinfo=None)


def _validate_session(db: Session, data: SessionCreate, exclude_id: int | None = None) -> None:
    movie = db.get(Movie, data.movie_id)
    if movie is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Movie not found")
    hall = db.get(CinemaHall, data.hall_id)
    if hall is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Hall not found")
    if not hall.is_active:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "Hall is closed")

    # A hall can only show one movie at a time.
    start = _naive(data.start_time)
    end = start + timedelta(minutes=movie.duration_minutes)
    for other in db.query(MovieSession).filter(MovieSession.hall_id == hall.id):
        if other.id == exclude_id:
            continue
        other_start = _naive(other.start_time)
        other_end = other_start + timedelta(minutes=other.movie.duration_minutes)
        if start < other_end and other_start < end:
            raise HTTPException(
                status.HTTP_409_CONFLICT,
                f"Hall is busy: session {other.id} runs {other_start:%Y-%m-%d %H:%M}–{other_end:%H:%M}",
            )


@router.get("/sessions/{session_id}", response_model=SessionRead)
def get_session(session_id: int, db: Session = Depends(get_db)):
    return _get_session(db, session_id)


@router.get("/sessions/{session_id}/seats", response_model=list[SeatStatus])
def get_session_seats(session_id: int, db: Session = Depends(get_db)):
    session = _get_session(db, session_id)
    seats = db.query(Seat).filter(Seat.hall_id == session.hall_id).order_by(Seat.row, Seat.number).all()
    booked = {sid for (sid,) in db.query(Ticket.seat_id).filter(Ticket.session_id == session_id)}
    return [
        SeatStatus(id=s.id, row=s.row, number=s.number, type=s.type, is_reserved=s.id in booked)
        for s in seats
    ]


@router.get("/admin/sessions", response_model=list[SessionRead], dependencies=[Depends(get_current_admin)])
def list_sessions(db: Session = Depends(get_db)):
    return db.query(MovieSession).order_by(MovieSession.start_time).all()


@router.post(
    "/admin/sessions",
    response_model=SessionRead,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(get_current_admin)],
)
def create_session(data: SessionCreate, db: Session = Depends(get_db)):
    _validate_session(db, data)
    session = MovieSession(**data.model_dump())
    db.add(session)
    db.commit()
    db.refresh(session)
    return session


@router.put("/admin/sessions/{session_id}", response_model=SessionRead, dependencies=[Depends(get_current_admin)])
def update_session(session_id: int, data: SessionCreate, db: Session = Depends(get_db)):
    session = _get_session(db, session_id)
    _validate_session(db, data, exclude_id=session_id)
    for key, value in data.model_dump().items():
        setattr(session, key, value)
    db.commit()
    db.refresh(session)
    return session


@router.delete(
    "/admin/sessions/{session_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(get_current_admin)],
)
def delete_session(session_id: int, db: Session = Depends(get_db)):
    session = _get_session(db, session_id)
    if db.query(Booking).filter(Booking.session_id == session_id).first():
        raise HTTPException(status.HTTP_409_CONFLICT, "Session has bookings and cannot be deleted")
    db.delete(session)
    db.commit()


@router.patch("/admin/sessions/{session_id}/price", response_model=SessionRead, dependencies=[Depends(get_current_admin)])
def update_session_price(session_id: int, price: float = Query(gt=0, le=100_000), db: Session = Depends(get_db)):
    session = _get_session(db, session_id)
    session.price = price
    db.commit()
    db.refresh(session)
    return session


@router.patch("/admin/sessions/price/bulk", dependencies=[Depends(get_current_admin)])
def bulk_update_prices(
    price: float = Query(gt=0, le=100_000),
    movie_id: int | None = None,
    hall_id: int | None = None,
    db: Session = Depends(get_db),
):
    if movie_id is None and hall_id is None:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "Give movie_id, hall_id or both")
    query = db.query(MovieSession)
    if movie_id is not None:
        query = query.filter(MovieSession.movie_id == movie_id)
    if hall_id is not None:
        query = query.filter(MovieSession.hall_id == hall_id)
    updated = query.update({MovieSession.price: price}, synchronize_session=False)
    db.commit()
    return {"updated": updated}

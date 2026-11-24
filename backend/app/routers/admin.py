from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import func
from sqlalchemy.orm import Session

from app.dependencies.auth import get_current_admin
from app.dependencies.db import get_db
from app.models import Booking, Movie, Ticket
from app.models import Session as MovieSession
from app.schemas.booking import BookingRead
from app.schemas.movie import MovieCreate, MovieRead
from app.services.booking import booking_to_read

router = APIRouter(prefix="/admin", tags=["Admin"], dependencies=[Depends(get_current_admin)])


def _get_movie(db: Session, movie_id: int) -> Movie:
    movie = db.get(Movie, movie_id)
    if movie is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Movie not found")
    return movie


@router.post("/movies", response_model=MovieRead, status_code=status.HTTP_201_CREATED)
def create_movie(data: MovieCreate, db: Session = Depends(get_db)):
    movie = Movie(**data.model_dump())
    db.add(movie)
    db.commit()
    db.refresh(movie)
    return movie


@router.put("/movies/{movie_id}", response_model=MovieRead)
def update_movie(movie_id: int, data: MovieCreate, db: Session = Depends(get_db)):
    movie = _get_movie(db, movie_id)
    for key, value in data.model_dump().items():
        setattr(movie, key, value)
    db.commit()
    db.refresh(movie)
    return movie


@router.delete("/movies/{movie_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_movie(movie_id: int, db: Session = Depends(get_db)):
    movie = _get_movie(db, movie_id)
    has_bookings = db.query(Booking).join(MovieSession).filter(MovieSession.movie_id == movie_id).first()
    if has_bookings:
        raise HTTPException(status.HTTP_409_CONFLICT, "Movie has bookings and cannot be deleted")
    db.delete(movie)
    db.commit()


@router.get("/dashboard")
def dashboard(db: Session = Depends(get_db)):
    return {
        "movies": db.query(Movie).count(),
        "sessions": db.query(MovieSession).count(),
        "bookings": db.query(Booking).count(),
        "tickets_sold": db.query(Ticket).count(),
        "revenue": round(db.query(func.coalesce(func.sum(Ticket.price), 0)).scalar(), 2),
    }


@router.get("/bookings", response_model=list[BookingRead])
def list_bookings(db: Session = Depends(get_db)):
    bookings = db.query(Booking).order_by(Booking.id.desc()).all()
    return [booking_to_read(b) for b in bookings]

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import models
from app.schemas.movie import MovieRead, MovieCreate
from app.dependencies.db import get_db
from app.dependencies.auth import get_current_admin

router = APIRouter(prefix="/admin", tags=["Admin"])

@router.post("/movies", response_model=MovieRead)
def create_movie(
    data: MovieCreate,
    db: Session = Depends(get_db),
    admin=Depends(get_current_admin)
):
    movie = models.Movie(**data.model_dump())

    db.add(movie)
    db.commit()
    db.refresh(movie)

    return movie


@router.put("/movies/{movie_id}", response_model=MovieRead)
def update_movie(
    movie_id: int,
    data: MovieCreate,
    db: Session = Depends(get_db),
    admin=Depends(get_current_admin)
):

    movie = db.query(models.Movie).filter(models.Movie.id == movie_id).first()

    if not movie:
        raise HTTPException(404, "Movie not found")
    
    update_data = data.model_dump(exclude_unset=True)

    for key, value in data.dict().items():
        setattr(movie, key, value)

    db.commit()

    return movie


@router.delete("/movies/{movie_id}")
def delete_movie(
    movie_id: int,
    db: Session = Depends(get_db),
    admin=Depends(get_current_admin)
):

    movie = db.query(models.Movie).filter(models.Movie.id == movie_id).first()

    if not movie:
        raise HTTPException(404, "Movie not found")

    db.delete(movie)
    db.commit()

    return {"message": "Deleted"}

@router.get("/dashboard")
def admin_dashboard(
    db: Session = Depends(get_db),
    admin=Depends(get_current_admin)
):

    movies = db.query(models.Movie).count()
    bookings = db.query(models.Booking).count()
    sessions = db.query(models.Session).count()

    return {
        "movies": movies,
        "bookings": bookings,
        "sessions": sessions
    }

@router.get("/bookings")
def get_bookings(
    db: Session = Depends(get_db),
    admin=Depends(get_current_admin)
):
    
    bookings = db.query(models.Booking).all()

    result = []

    for booking in bookings:

        session = booking.session
        movie = session.movie

        for ticket in booking.tickets:

            seat = ticket.seat

            result.append({
                "booking_id": booking.id,
                "booking_code": booking.booking_code,
                "customer_name": booking.customer_name,

                "movie_title": movie.title,
                "session_time": session.start_time,

                "seat_row": seat.row,
                "seat_number": seat.number,
                "seat_type": seat.type  
            })

    return result
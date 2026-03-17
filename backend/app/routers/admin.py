from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import models
from app.schemas.movie import MovieRead, MovieCreate
from app.dependencies.db import get_db
from app.dependencies.auth import get_current_admin

router = APIRouter(tags=["Admin"])

@router.post("/movies", response_model=MovieRead)
def create_movie(
    data: MovieCreate,
    db: Session = Depends(get_db),
    admin=Depends(get_current_admin)
):
    movie = models.Movie(**data.dict())

    db.add(movie)
    db.commit()
    db.refresh(movie)

    return movie


@router.put("/movies/{movie_id}")
def update_movie(
    movie_id: int,
    data: MovieCreate,
    db: Session = Depends(get_db),
    admin=Depends(get_current_admin)
):

    movie = db.query(models.Movie).filter(models.Movie.id == movie_id).first()

    if not movie:
        raise HTTPException(404, "Movie not found")

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
def get_bookings(db: Session = Depends(get_db)):
    bookings = db.query(models.Booking).all()

    return bookings
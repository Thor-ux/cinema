from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.dependencies.db import get_db
from app.models import Movie
from app.models import Session as MovieSession
from app.schemas.movie import MovieRead
from app.schemas.session import SessionRead

router = APIRouter(prefix="/movies", tags=["Movies"])


@router.get("", response_model=list[MovieRead])
def list_movies(db: Session = Depends(get_db)):
    return db.query(Movie).order_by(Movie.title).all()


@router.get("/{movie_id}", response_model=MovieRead)
def get_movie(movie_id: int, db: Session = Depends(get_db)):
    movie = db.get(Movie, movie_id)
    if movie is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Movie not found")
    return movie


@router.get("/{movie_id}/showtimes", response_model=list[SessionRead])
def get_showtimes(movie_id: int, db: Session = Depends(get_db)):
    if db.get(Movie, movie_id) is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Movie not found")
    return (
        db.query(MovieSession)
        .filter(MovieSession.movie_id == movie_id)
        .order_by(MovieSession.start_time)
        .all()
    )

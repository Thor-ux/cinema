from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import models, schemas
from app.dependencies import get_db

router = APIRouter(prefix="/movies", tags=["Movies"])


@router.get("/", response_model=list[schemas.Movie])
def get_movies(db: Session = Depends(get_db)):
    return db.query(models.Movie).all()


@router.get("/{movie_id}", response_model=schemas.Movie)
def get_movie(movie_id: int, db: Session = Depends(get_db)):
    movie = db.query(models.Movie).filter(models.Movie.id == movie_id).first()
    if not movie:
        raise HTTPException(status_code=404, detail="Movie not found")
    return movie
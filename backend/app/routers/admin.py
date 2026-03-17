from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import models, schemas
from app.dependencies import get_db

router = APIRouter(prefix="/admin", tags=["Admin"])


@router.post("/movies", response_model=schemas.Movie)
def create_movie(data: schemas.MovieCreate, db: Session = Depends(get_db)):
    movie = models.Movie(**data.dict())
    db.add(movie)
    db.commit()
    db.refresh(movie)
    return movie


@router.delete("/movies/{movie_id}")
def delete_movie(movie_id: int, db: Session = Depends(get_db)):
    movie = db.query(models.Movie).filter(models.Movie.id == movie_id).first()
    if not movie:
        raise HTTPException(404)
    db.delete(movie)
    db.commit()
    return {"message": "Deleted"}
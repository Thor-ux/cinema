from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.dependencies.db import get_db
from app.models.movie import Movie

router = APIRouter(tags=["Movies"])

@router.get("/movies")
def get_movies(db: Session = Depends(get_db)):
    return db.query(Movie).all()
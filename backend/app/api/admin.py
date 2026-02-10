from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.movie import Movie
from app.schemas import MovieCreate

router = APIRouter(prefix="/admin", tags=["Admin"])


@router.post("/movies")
def create_movie(movie: MovieCreate, db: Session = Depends(get_db)):
    m = Movie(**movie.dict())
    db.add(m)
    db.commit()
    db.refresh(m)
    return m
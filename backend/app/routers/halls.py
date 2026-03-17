from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.dependencies.db import get_db
from app.dependencies.auth import get_current_admin
from app.models.hall import CinemaHall
from app.models.seat import Seat
from app.schemas.hall import HallCreate

router = APIRouter(tags=["Halls"])


# Create hall
@router.post("/")
def create_hall(data: HallCreate, db: Session = Depends(get_db)):

    hall = CinemaHall(**data.dict())

    db.add(hall)
    db.commit()
    db.refresh(hall)

    # generate seats
    for r in range(1, hall.rows + 1):
        for s in range(1, hall.seats_per_row + 1):
            seat = Seat(
                hall_id=hall.id,
                row=r,
                number=s
            )
            db.add(seat)

    db.commit()

    return hall

@router.get("/")
def get_halls(db: Session = Depends(get_db)):
    return db.query(CinemaHall).all()

@router.put("/{hall_id}")
def update_hall(hall_id: int, data: HallCreate, db: Session = Depends(get_db)):

    hall = db.query(CinemaHall).filter(CinemaHall.id == hall_id).first()

    if not hall:
        raise HTTPException(404, "Hall not found")

    for key, value in data.dict().items():
        setattr(hall, key, value)

    db.commit()
    return hall

@router.delete("/{hall_id}")
def delete_hall(hall_id: int, db: Session = Depends(get_db)):

    hall = db.query(CinemaHall).filter(CinemaHall.id == hall_id).first()

    if not hall:
        raise HTTPException(404, "Hall not found")

    db.delete(hall)
    db.commit()

    return {"message": "Hall deleted"}
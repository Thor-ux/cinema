from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.hall import CinemaHall
from app.schemas.hall import HallCreate

router = APIRouter(prefix="/admin/halls")

@router.post("/")
def create_hall(data: HallCreate, db: Session = Depends(get_db)):
    hall = CinemaHall(**data.dict())
    db.add(hall)
    db.commit()
    return hall

def generate_seats(db, hall):
    for row in range(1, hall.rows + 1):
        for number in range(1, hall.seats_per_row + 1):
            seat = Seat(
                hall_id=hall.id,
                row=row,
                number=number,
                type="standard"
            )
            db.add(seat)
    db.commit()
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.dependencies.db import get_db
from app.models.hall import CinemaHall
from app.models.seat import Seat
from app.schemas.hall import HallCreate

router = APIRouter(prefix="/halls", tags=["Halls"])

@router.post("/")
def create_hall(
    data: HallCreate,
    db: Session = Depends(get_db)
):

    hall = CinemaHall(
        name=data.name,
        rows=data.rows,
        seats_per_row=data.seats_per_row
    )

    db.add(hall)
    db.commit()
    db.refresh(hall)

    vip_set = {
        (seat.row, seat.number)
        for seat in data.vip_seats
    }

    seats = []

    for row in range(1, data.rows + 1):
        for number in range(1, data.seats_per_row + 1):

            seat_type = "vip" if (row, number) in vip_set else "standard"

            seat = Seat(
                hall_id=hall.id,
                row=row,
                number=number,
                type=seat_type
            )

            seats.append(seat)

    db.add_all(seats)
    db.commit()

    return {
        "message": "Hall created",
        "hall_id": hall.id,
        "total_seats": len(seats),
        "vip_seats": len(vip_set)
    }

@router.get("/")
def get_halls(db: Session = Depends(get_db)):
    return db.query(CinemaHall).all()

@router.put("/{hall_id}")
def update_hall(hall_id: int, data: HallCreate, db: Session = Depends(get_db)):

    hall = db.query(CinemaHall).filter(CinemaHall.id == hall_id).first()

    if not hall:
        raise HTTPException(404, "Hall not found")

    for key, value in data.update_hall.items():
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
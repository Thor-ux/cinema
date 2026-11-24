from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.dependencies.auth import get_current_admin
from app.dependencies.db import get_db
from app.models import Booking, CinemaHall, Seat
from app.models import Session as MovieSession
from app.schemas.hall import HallCreate, HallRead, HallUpdate

router = APIRouter(prefix="/admin/halls", tags=["Halls"], dependencies=[Depends(get_current_admin)])


def _get_hall(db: Session, hall_id: int) -> CinemaHall:
    hall = db.get(CinemaHall, hall_id)
    if hall is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Hall not found")
    return hall


@router.get("", response_model=list[HallRead])
def list_halls(db: Session = Depends(get_db)):
    return db.query(CinemaHall).order_by(CinemaHall.id).all()


@router.post("", status_code=status.HTTP_201_CREATED)
def create_hall(data: HallCreate, db: Session = Depends(get_db)):
    hall = CinemaHall(name=data.name, rows=data.rows, seats_per_row=data.seats_per_row)
    db.add(hall)
    db.flush()

    vip = {(s.row, s.number) for s in data.vip_seats}
    db.add_all(
        Seat(hall_id=hall.id, row=r, number=n, type="vip" if (r, n) in vip else "standard")
        for r in range(1, data.rows + 1)
        for n in range(1, data.seats_per_row + 1)
    )
    db.commit()
    return {"hall_id": hall.id, "total_seats": data.rows * data.seats_per_row, "vip_seats": len(vip)}


@router.patch("/{hall_id}", response_model=HallRead)
def update_hall(hall_id: int, data: HallUpdate, db: Session = Depends(get_db)):
    hall = _get_hall(db, hall_id)
    for key, value in data.model_dump(exclude_unset=True).items():
        setattr(hall, key, value)
    db.commit()
    db.refresh(hall)
    return hall


@router.delete("/{hall_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_hall(hall_id: int, db: Session = Depends(get_db)):
    hall = _get_hall(db, hall_id)
    has_bookings = db.query(Booking).join(MovieSession).filter(MovieSession.hall_id == hall_id).first()
    if has_bookings:
        raise HTTPException(status.HTTP_409_CONFLICT, "Hall has bookings; close it instead (is_active=false)")
    db.delete(hall)
    db.commit()

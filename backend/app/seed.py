"""Fill an empty database with demo movies, halls and a week of sessions.

Usage:  python -m app.seed
"""
from datetime import datetime, time, timedelta, timezone

from app import models  # noqa: F401
from app.database import Base, SessionLocal, engine
from app.models import CinemaHall, Movie, Seat, Session

MOVIES = [
    ("The Last Orbit", "A stranded crew has 48 hours to bring their station home.", 124),
    ("Paper Lanterns", "Two strangers keep meeting at the same night market.", 98),
    ("Iron Valley", "A mining town stands up to the company that owns it.", 131),
    ("Small Hours", "A late-night radio host takes a call that changes everything.", 105),
]
HALLS = [("Hall 1", 8, 12, {7, 8}), ("Hall 2 · VIP", 5, 8, {1, 2, 3, 4, 5})]  # name, rows, seats/row, VIP rows
SHOW_TIMES = [time(12, 0), time(15, 30), time(19, 0), time(22, 15)]


def main() -> None:
    Base.metadata.create_all(bind=engine)
    with SessionLocal() as db:
        if db.query(Movie).first():
            print("Database already has data; nothing to do.")
            return

        movies = [Movie(title=t, description=d, duration_minutes=m) for t, d, m in MOVIES]
        db.add_all(movies)
        halls = []
        for name, rows, per_row, vip_rows in HALLS:
            hall = CinemaHall(name=name, rows=rows, seats_per_row=per_row)
            db.add(hall)
            db.flush()
            db.add_all(
                Seat(hall_id=hall.id, row=r, number=n, type="vip" if r in vip_rows else "standard")
                for r in range(1, rows + 1)
                for n in range(1, per_row + 1)
            )
            halls.append(hall)
        db.flush()

        today = datetime.now(timezone.utc).date()
        for day in range(7):
            for i, slot in enumerate(SHOW_TIMES):
                for h, hall in enumerate(halls):
                    movie = movies[(day + i + h) % len(movies)]
                    start = datetime.combine(today + timedelta(days=day), slot, tzinfo=timezone.utc)
                    price = 450.0 if slot >= time(18, 0) else 350.0
                    db.add(Session(movie_id=movie.id, hall_id=hall.id, start_time=start, price=price))
        db.commit()
        print(f"Added {len(movies)} movies, {len(halls)} halls and {7 * len(SHOW_TIMES) * len(halls)} sessions.")


if __name__ == "__main__":
    main()

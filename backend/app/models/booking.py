from sqlalchemy import Column, Integer, ForeignKey, String, DateTime, UniqueConstraint
from datetime import datetime
from app.database import Base

class Booking(Base):
    __tablename__ = "bookings"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    showtime_id = Column(Integer, ForeignKey("showtimes.id"))
    seat_id = Column(Integer, ForeignKey("seats.id"))
    status = Column(String, default="HELD")
    created_at = Column(DateTime, default=datetime.utcnow)

    __table_args__ = (
        UniqueConstraint("showtime_id", "seat_id"),
    )

from sqlalchemy import Column, ForeignKey, Integer, String, UniqueConstraint
from sqlalchemy.orm import relationship

from app.database import Base


class Seat(Base):
    __tablename__ = "seats"
    __table_args__ = (UniqueConstraint("hall_id", "row", "number", name="uq_seat_position"),)

    id = Column(Integer, primary_key=True)
    hall_id = Column(Integer, ForeignKey("halls.id", ondelete="CASCADE"), nullable=False)
    row = Column(Integer, nullable=False)
    number = Column(Integer, nullable=False)
    type = Column(String(20), nullable=False, default="standard")

    hall = relationship("CinemaHall", back_populates="seats")

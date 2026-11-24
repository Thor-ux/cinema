from sqlalchemy import Boolean, Column, Integer, String
from sqlalchemy.orm import relationship

from app.database import Base


class CinemaHall(Base):
    __tablename__ = "halls"

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    rows = Column(Integer, nullable=False)
    seats_per_row = Column(Integer, nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)

    seats = relationship("Seat", back_populates="hall", cascade="all, delete-orphan")
    sessions = relationship("Session", back_populates="hall", cascade="all, delete-orphan")

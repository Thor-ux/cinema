from sqlalchemy import Column, DateTime, Float, ForeignKey, Integer
from sqlalchemy.orm import relationship

from app.database import Base


class Session(Base):
    """A screening: one movie in one hall at one time."""

    __tablename__ = "sessions"

    id = Column(Integer, primary_key=True)
    movie_id = Column(Integer, ForeignKey("movies.id", ondelete="CASCADE"), nullable=False)
    hall_id = Column(Integer, ForeignKey("halls.id", ondelete="CASCADE"), nullable=False)
    start_time = Column(DateTime(timezone=True), nullable=False)
    price = Column(Float, nullable=False)

    movie = relationship("Movie", back_populates="sessions")
    hall = relationship("CinemaHall", back_populates="sessions")
    bookings = relationship("Booking", back_populates="session", cascade="all, delete-orphan")

from sqlalchemy import Column, Integer, DateTime, ForeignKey, Float, Index
from app.database import Base


class Showtime(Base):
    __tablename__ = "showtimes"

    id = Column(Integer, primary_key=True, index=True)

    movie_id = Column(Integer, ForeignKey("movies.id", ondelete="CASCADE"), nullable=False)
    hall_id = Column(Integer, ForeignKey("cinema_halls.id", ondelete="CASCADE"), nullable=False)

    start_time = Column(DateTime, nullable=False)
    price = Column(Float, nullable=False)

    __table_args__ = (
        Index("idx_showtime_hall_time", "hall_id", "start_time"),
    )

from sqlalchemy import Column, Integer, DateTime, ForeignKey, Float
from app.database import Base

class Showtime(Base):
    __tablename__ = "showtimes"

    id = Column(Integer, primary_key=True)
    movie_id = Column(Integer, ForeignKey("movies.id"))
    hall_id = Column(Integer, ForeignKey("halls.id"))
    start_time = Column(DateTime)
    price = Column(Float)

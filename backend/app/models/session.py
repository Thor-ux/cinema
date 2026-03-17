from sqlalchemy import Column, Integer, ForeignKey, DateTime, Float
from app.database import Base

class Session(Base):

    __tablename__ = "sessions"

    id = Column(Integer, primary_key=True)

    movie_id = Column(Integer, ForeignKey("movies.id"))
    hall_id = Column(Integer, ForeignKey("halls.id"))

    start_time = Column(DateTime)
    price = Column(Float)
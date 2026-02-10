from sqlalchemy import Column, Integer, String
from app.database import Base

class CinemaHall(Base):
    __tablename__ = "cinema_halls"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    rows = Column(Integer, nullable=False)
    cols = Column(Integer, nullable=False)

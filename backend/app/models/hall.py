from sqlalchemy import Column, Integer, String, Boolean
from app.database import Base

class CinemaHall(Base):

    __tablename__ = "halls"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    rows = Column(Integer)
    seats_per_row = Column(Integer)
    is_active = Column(Boolean, default=True)
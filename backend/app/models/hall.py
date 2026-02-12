from sqlalchemy import Column, Integer
from app.database import Base

class Hall(Base):
    __tablename__ = "halls"

    id = Column(Integer, primary_key=True)
    rows = Column(Integer, nullable=False)
    seats_per_row = Column(Integer, nullable=False)

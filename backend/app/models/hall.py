from sqlalchemy import Column, Integer
from app.database import Base

class Hall(Base):
    __tablename__ = "halls"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False) # new
    rows = Column(Integer, nullable=False)
    seats_per_row = Column(Integer, nullable=False)
    is_active = Column(Boolean, default=True) # new

    seats = relationship("Seat", back_populates="hall", cascade="all, delete")

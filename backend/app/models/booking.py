from sqlalchemy import Column, Integer, ForeignKey, String, DateTime, UniqueConstraint
from datetime import datetime
from app.database import Base

class Booking(Base):
    __tablename__ = "bookings"

    id = Column(Integer, primary_key=True)
    booking_code = Column(String, unique=True, index=True)  
    created_at = Column(DateTime, default=datetime.utcnow)

    tickets = relationship("Ticket", back_populates="booking")

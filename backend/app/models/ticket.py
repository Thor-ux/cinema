from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from datetime import datetime
from app.database import Base

class Ticket(Base):
    __tablename__ = "tickets"

    id = Column(Integer, primary_key=True)
    seat_id = Column(Integer, nullable=False)
    showtime_id = Column(Integer, nullable=False)
    status = Column(String, default="HELD")
    expires_at = Column(DateTime)
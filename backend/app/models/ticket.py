from sqlalchemy import Column, Integer, ForeignKey, String
from app.database import Base

class Ticket(Base):
    __tablename__ = "tickets"

    id = Column(Integer, primary_key=True)
    booking_id = Column(Integer, ForeignKey("bookings.id"))
    qr_code = Column(String)

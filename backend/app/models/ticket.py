from sqlalchemy import Column, Integer, ForeignKey, String
from app.database import Base

class Ticket(Base):
    __tablename__ = "tickets"

    id = Column(Integer, primary_key=True)
    booking_id = Column(Integer, ForeignKey("bookings.id"))
    showtime_id = Column(Integer, ForeignKey("showtimes.id"))
    seat_id = Column(Integer, ForeignKey("seats.id"))

    qr_code = Column(String)

    booking = relationship("Booking", back_populates="tickets")

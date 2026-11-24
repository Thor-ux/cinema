from sqlalchemy import Column, Float, ForeignKey, Integer, Text, UniqueConstraint
from sqlalchemy.orm import relationship

from app.database import Base


class Ticket(Base):
    __tablename__ = "tickets"
    # The database itself refuses a second ticket for the same seat in the same
    # session, so two simultaneous requests can never double-book a seat.
    __table_args__ = (UniqueConstraint("session_id", "seat_id", name="uq_ticket_session_seat"),)

    id = Column(Integer, primary_key=True)
    booking_id = Column(Integer, ForeignKey("bookings.id", ondelete="CASCADE"), nullable=False)
    session_id = Column(Integer, ForeignKey("sessions.id", ondelete="CASCADE"), nullable=False)
    seat_id = Column(Integer, ForeignKey("seats.id", ondelete="CASCADE"), nullable=False)
    price = Column(Float, nullable=False)
    qr_code = Column(Text, nullable=False)  # base64-encoded PNG

    booking = relationship("Booking", back_populates="tickets")
    seat = relationship("Seat")

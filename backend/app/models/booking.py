from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from app.database import Base


class Booking(Base):

    __tablename__ = "bookings"

    id = Column(Integer, primary_key=True)

    session_id = Column(
        Integer,
        ForeignKey("sessions.id")
    )

    user_id = Column(
        Integer,
        ForeignKey("users.id")
    )

    customer_name = Column(String)

    booking_code = Column(
        String,
        unique=True
    )

    session = relationship(
        "Session",
        back_populates="bookings"
    )

    user = relationship(
        "User",
        back_populates="bookings"
    )

    tickets = relationship(
        "Ticket",
        back_populates="booking",
        cascade="all, delete"
    )
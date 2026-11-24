from sqlalchemy import Boolean, Column, Integer, String
from sqlalchemy.orm import relationship

from app.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    email = Column(String(255), unique=True, nullable=False, index=True)
    password = Column(String(255), nullable=False)  # bcrypt hash
    is_admin = Column(Boolean, default=False, nullable=False)

    bookings = relationship("Booking", back_populates="user", cascade="all, delete-orphan")

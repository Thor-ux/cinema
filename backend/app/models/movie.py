from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from app.database import Base


class Movie(Base):
    __tablename__ = "movies"

    id = Column(Integer, primary_key=True)
    title = Column(String(255), nullable=False)
    description = Column(String)
    duration_minutes = Column(Integer, nullable=False)

    sessions = relationship("Session", back_populates="movie", cascade="all, delete-orphan")

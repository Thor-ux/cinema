from sqlalchemy import Column, Integer, ForeignKey, String
from app.database import Base

class Seat(Base):

    __tablename__ = "seats"

    id = Column(Integer, primary_key=True)

    hall_id = Column(Integer, ForeignKey("halls.id"))

    row = Column(Integer)
    number = Column(Integer)
    type = Column(String, default="standard")
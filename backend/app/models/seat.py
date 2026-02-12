from sqlalchemy import Column, Integer, ForeignKey, UniqueConstraint
from app.database import Base

class Seat(Base):
    __tablename__ = "seats"

    id = Column(Integer, primary_key=True)
    hall_id = Column(Integer, ForeignKey("halls.id"))
    row = Column(Integer)
    number = Column(Integer)

    __table_args__ = (
        UniqueConstraint("hall_id", "row", "number"),
    )

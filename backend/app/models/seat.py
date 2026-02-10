from sqlalchemy import Column, Integer, Boolean, ForeignKey, UniqueConstraint
from app.database import Base


class Seat(Base):
    __tablename__ = "seats"

    id = Column(Integer, primary_key=True, index=True)
    hall_id = Column(Integer, ForeignKey("cinema_halls.id", ondelete="CASCADE"), nullable=False)

    row = Column(Integer, nullable=False)
    number = Column(Integer, nullable=False)

    is_vip = Column(Boolean, default=False, nullable=False)

    __table_args__ = (
        UniqueConstraint("hall_id", "row", "number", name="unique_seat_per_hall"),
    )

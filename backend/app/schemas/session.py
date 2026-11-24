from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class SessionCreate(BaseModel):
    movie_id: int
    hall_id: int
    start_time: datetime
    price: float = Field(gt=0, le=100_000)


class SessionRead(SessionCreate):
    model_config = ConfigDict(from_attributes=True)
    id: int


class SeatStatus(BaseModel):
    id: int
    row: int
    number: int
    type: str
    is_reserved: bool

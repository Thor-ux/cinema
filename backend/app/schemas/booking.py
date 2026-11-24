from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class BookingCreate(BaseModel):
    session_id: int
    seat_ids: list[int] = Field(min_length=1, max_length=10)
    customer_name: str = Field(min_length=1, max_length=100)


class TicketRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    seat_id: int
    row: int
    number: int
    seat_type: str
    price: float
    qr_code: str


class BookingRead(BaseModel):
    id: int
    booking_code: str
    customer_name: str
    session_id: int
    movie_title: str
    start_time: datetime
    hall_name: str
    total_price: float
    tickets: list[TicketRead]

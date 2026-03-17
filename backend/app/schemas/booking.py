from pydantic import BaseModel
from typing import List

class BookingCreate(BaseModel):

    session_id: int
    seat_ids: List[int]
    customer_name: str
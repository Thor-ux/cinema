from pydantic import BaseModel, Field
from typing import List


class VIPSeat(BaseModel):
    row: int
    number: int


class HallCreate(BaseModel):
    name: str
    rows: int = Field(gt=0)
    seats_per_row: int = Field(gt=0)

    vip_seats: List[VIPSeat] = []
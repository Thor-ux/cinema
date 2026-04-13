from pydantic import BaseModel

class HallCreate(BaseModel):
    name: str
    rows: int
    seats_per_row: int
    vip_rows: int = 0
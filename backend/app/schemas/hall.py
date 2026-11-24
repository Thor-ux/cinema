from pydantic import BaseModel, ConfigDict, Field, model_validator


class VIPSeat(BaseModel):
    row: int = Field(gt=0)
    number: int = Field(gt=0)


class HallCreate(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    rows: int = Field(gt=0, le=50)
    seats_per_row: int = Field(gt=0, le=60)
    vip_seats: list[VIPSeat] = []

    @model_validator(mode="after")
    def vip_seats_inside_hall(self):
        for seat in self.vip_seats:
            if seat.row > self.rows or seat.number > self.seats_per_row:
                raise ValueError(f"VIP seat row {seat.row}, number {seat.number} is outside the hall")
        return self


class HallUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=100)
    is_active: bool | None = None


class HallRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    name: str
    rows: int
    seats_per_row: int
    is_active: bool

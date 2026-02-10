from pydantic import BaseModel, Field


class MovieCreate(BaseModel):
    title: str = Field(min_length=2)
    description: str | None = None
    duration_minutes: int = Field(gt=0)


class MovieRead(MovieCreate):
    id: int

    class Config:
        orm_mode = True

from pydantic import BaseModel, Field


class MovieCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=255)
    description: str | None = None
    duration_minutes: int = Field(..., gt=0, lt=500)


class MovieRead(MovieCreate):
    id: int

    class Config:
        from_attributes = True

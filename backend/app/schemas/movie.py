from pydantic import BaseModel, ConfigDict, Field


class MovieCreate(BaseModel):
    title: str = Field(min_length=1, max_length=255)
    description: str | None = Field(default=None, max_length=2000)
    duration_minutes: int = Field(gt=0, lt=500)


class MovieRead(MovieCreate):
    model_config = ConfigDict(from_attributes=True)
    id: int

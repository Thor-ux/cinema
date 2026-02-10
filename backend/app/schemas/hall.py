from pydantic import BaseModel, Field

class HallCreate(BaseModel):
    name: str = Field(min_length=2)
    rows: int = Field(gt=0)
    cols: int = Field(gt=0)

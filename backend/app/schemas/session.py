from pydantic import BaseModel, Field
from datetime import datetime

class SessionCreate(BaseModel):

    movie_id: int
    hall_id: int
    start_time: datetime
    price: float = Field(gt=0)
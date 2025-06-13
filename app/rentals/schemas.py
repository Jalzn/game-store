from datetime import datetime
from pydantic import BaseModel
from typing import Optional


class RentalCreate(BaseModel):
    customer_id: int
    game_id: int


class RentalReturn(BaseModel):
    return_date: Optional[datetime] = None


class RentalRead(BaseModel):
    id: int
    customer_id: int
    game_id: int
    rental_date: datetime
    return_date: Optional[datetime] = None

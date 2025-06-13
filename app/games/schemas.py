from pydantic import BaseModel
from typing import Optional


class GameCreate(BaseModel):
    title: str
    genre: str
    platform: str
    price: float


class GameUpdate(BaseModel):
    title: Optional[str] = None
    genre: Optional[str] = None
    platform: Optional[str] = None
    price: Optional[float] = None

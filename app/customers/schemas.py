from typing import Optional
from pydantic import BaseModel


class CustomerCreate(BaseModel):
    name: str
    email: str
    phone: str


class CustomerUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None

from datetime import datetime
from sqlmodel import Field, SQLModel


class Customer(SQLModel, table=True):
    __tablename__ = "customers"

    id: int = Field(primary_key=True)
    name: str = Field(min_length=1, max_length=255, nullable=False)
    email: str = Field(min_length=1, max_length=255, unique=True, nullable=False)
    phone: str = Field(min_length=1, max_length=255, unique=True, nullable=False)
    created_at: datetime = Field(nullable=False, default_factory=datetime.now)

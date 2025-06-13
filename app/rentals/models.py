from datetime import datetime
from sqlmodel import SQLModel, Field


class Rental(SQLModel, table=True):
    __tablename__ = "rentals"

    id: int = Field(default=None, primary_key=True)
    customer_id: int = Field(foreign_key="customers.id")
    game_id: int = Field(foreign_key="games.id")
    rental_date: datetime = Field(default_factory=datetime.now)
    return_date: datetime | None = None

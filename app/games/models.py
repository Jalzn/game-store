from sqlmodel import SQLModel, Field


class Game(SQLModel, table=True):
    __tablename__ = "games"

    id: int = Field(default=None, primary_key=True)
    title: str
    genre: str
    platform: str
    price: float

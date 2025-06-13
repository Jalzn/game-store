from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.api import customers, games, rentals
from app.database import create_db_and_tables


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield


app = FastAPI(title="Game Store API", lifespan=lifespan)

app.include_router(customers.router)
app.include_router(games.router)
app.include_router(rentals.router)

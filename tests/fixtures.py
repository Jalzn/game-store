from pytest import fixture
from sqlmodel import SQLModel, Session, create_engine
from app.customers import models
from app.games import models
from app.rentals import models


@fixture(name="session")
def session():
    engine = create_engine("sqlite://")
    SQLModel.metadata.create_all(engine)

    with Session(engine) as session:
        yield session

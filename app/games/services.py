from typing import List
from sqlmodel import Session, select

from app.games.models import Game
from app.games.schemas import GameCreate, GameUpdate
from app.games.exceptions import GameNotFoundException, GameAlreadyExistsException


class GameService:
    def __init__(self, session: Session):
        self.session = session

    def create_game(self, schema: GameCreate) -> Game:
        if self.exists_by_title(schema.title):
            raise GameAlreadyExistsException

        game = Game(
            title=schema.title,
            genre=schema.genre,
            platform=schema.platform,
            price=schema.price,
        )
        self.session.add(game)
        self.session.commit()
        self.session.refresh(game)
        return game

    def get_by_id(self, game_id: int) -> Game:
        game = self.session.get(Game, game_id)
        if not game:
            raise GameNotFoundException
        return game

    def list_all(self) -> List[Game]:
        return list(self.session.exec(select(Game)))

    def update_game(self, game_id: int, schema: GameUpdate) -> Game:
        game = self.get_by_id(game_id)

        if (
            schema.title
            and schema.title != game.title
            and self.exists_by_title(schema.title)
        ):
            raise GameAlreadyExistsException

        if schema.title:
            game.title = schema.title
        if schema.genre:
            game.genre = schema.genre
        if schema.platform:
            game.platform = schema.platform
        if schema.price is not None:
            game.price = schema.price

        self.session.add(game)
        self.session.commit()
        self.session.refresh(game)
        return game

    def delete_game(self, game_id: int) -> None:
        game = self.get_by_id(game_id)
        self.session.delete(game)
        self.session.commit()

    def exists_by_title(self, title: str) -> bool:
        game = self.session.exec(select(Game).where(Game.title == title)).first()
        return True if game else False

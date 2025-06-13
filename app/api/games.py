from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session
from app.database import get_session
from app.games.schemas import GameCreate, GameUpdate
from app.games.services import GameService
from app.games.exceptions import GameAlreadyExistsException, GameNotFoundException

router = APIRouter(prefix="/games", tags=["games"])


@router.post("/")
def create_game(schema: GameCreate, session: Session = Depends(get_session)):
    service = GameService(session)
    try:
        game = service.create_game(schema)
        return game
    except GameAlreadyExistsException:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="Game already exists"
        )


@router.get("/")
def list_games(session: Session = Depends(get_session)):
    service = GameService(session)
    return service.list_all()


@router.put("/{game_id}")
def update_game(
    game_id: int, schema: GameUpdate, session: Session = Depends(get_session)
):
    service = GameService(session)
    try:
        return service.update_game(game_id, schema)
    except GameNotFoundException:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Game not found"
        )


@router.delete("/{game_id}")
def delete_game(game_id: int, session: Session = Depends(get_session)):
    service = GameService(session)
    try:
        service.delete_game(game_id)
        return {"detail": "Game deleted"}
    except GameNotFoundException:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Game not found"
        )

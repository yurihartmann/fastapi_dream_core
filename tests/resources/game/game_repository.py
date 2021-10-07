from sqlmodel import Session

from fastapi_dream_core import BaseRepository
from tests.resources.game.game_model_mixin import GameModel


class GameRepository(BaseRepository):

    def __init__(self, session: Session):
        super().__init__(session=session, model=GameModel)

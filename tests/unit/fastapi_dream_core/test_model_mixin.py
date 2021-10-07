import unittest

from sqlalchemy import create_engine
from sqlmodel import SQLModel, Session

from tests.resources.game.game_repository import GameRepository


class TestModelMixin(unittest.IsolatedAsyncioTestCase):

    async def setUp(self) -> None:
        engine = create_engine("sqlite:///:memory:")
        SQLModel.metadata.create_all(engine)
        self.session = Session(engine)
        self.game_repository = GameRepository(session=self.session)

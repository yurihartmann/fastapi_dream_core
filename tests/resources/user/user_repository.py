from sqlmodel import Session

from fastapi_dream_core import BaseRepository
from tests.resources.user.user_model import UserModel


class UserRepository(BaseRepository):

    def __init__(self, session: Session):
        super().__init__(session=session, model=UserModel)

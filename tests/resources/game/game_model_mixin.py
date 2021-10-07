from typing import Optional

from sqlmodel import SQLModel, Field

from fastapi_dream_core import ModelMixin


class GameModel(SQLModel, ModelMixin, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str

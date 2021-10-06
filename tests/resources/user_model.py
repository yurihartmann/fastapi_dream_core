from typing import Optional

from sqlmodel import Field, SQLModel


class UserModel(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    age: Optional[int] = None

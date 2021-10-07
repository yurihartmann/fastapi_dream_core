from typing import Optional

from pydantic import BaseModel
from sqlmodel import Field, SQLModel


class UserModel(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    age: Optional[int] = None


class CreateUserSchema(BaseModel):
    name: str
    age: int


class UpdateUserSchema(BaseModel):
    name: str
    age: int

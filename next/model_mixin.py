from abc import ABC
from datetime import datetime

from sqlalchemy.orm import declared_attr
from sqlmodel import SQLModel


class ModelMixin(SQLModel):
    __name__: str
    __config__ = {}

    # Generate __tablename__ automatically
    @declared_attr
    def __tablename__(cls) -> str:
        return cls.__name__.lower()

    created_at: datetime = Field(default_factory=datetime.utcnow)
    update_at: datetime = Field(default=datetime.utcnow)
    deleted_at: datetime = Field(default=None, nullable=True)



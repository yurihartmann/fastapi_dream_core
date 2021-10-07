from abc import ABC
from datetime import datetime
from typing import Any

from sqlalchemy.orm import declared_attr
from sqlmodel import Field


class SimpleModelMixin(ABC):
    id: Any
    __name__: str

    # Generate __tablename__ automatically
    @declared_attr
    def __tablename__(cls) -> str:
        return cls.__name__.lower()


class TimestampModelMixin(ABC):
    created_at: datetime = Field(default_factory=datetime.utcnow)
    update_at: datetime = Field(default=datetime.utcnow)
    deleted_at: datetime = Field(default=None, nullable=True)


class ModelMixin(SimpleModelMixin, TimestampModelMixin):
    __config__ = {}

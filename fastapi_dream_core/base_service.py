from abc import ABC

from pydantic import BaseModel
from sqlmodel import Session, SQLModel

from fastapi_dream_core import BaseRepository
from fastapi_dream_core.base_repository import ModelType


class BaseService(ABC):

    __base_model__: SQLModel
    session: Session
    Model: ModelType
    CreateSchemaType: BaseModel
    UpdateSchemaType: BaseModel
    base_repository: BaseRepository

    def __call__(self, *args, **kwargs):
        if not self.__base_model__:
            raise Exception('__base_model__ faltando')

    async def get_by_id(self, id: int) -> ModelType:
        return await self.base_repository.get_one_by_filters(
            filters={
                'id': id
            }
        )

    async def create(self, create_model) -> ModelType:
        return await self.base_repository.create(
            obj_in=create_model
        )

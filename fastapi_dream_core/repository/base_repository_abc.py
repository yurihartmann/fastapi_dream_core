from abc import ABC
from typing import Any, Optional, Dict, Union, List

from fastapi_dream_core.pagination import PageQuery, Page
from fastapi_dream_core.constants import ModelType, CreateSchemaType, UpdateSchemaType


class BaseRepositoryABC(ABC):

    async def find_one_by_filters(self, filters: Dict[str, Any] = None) -> Optional[ModelType]:
        """Not Implemented"""

    async def find_by_filters_paginated(
            self,
            page_query: PageQuery = PageQuery(),
            filters: dict = None,
            order: str = 'id',
            desc: bool = False
    ) -> Page:
        """Not Implemented"""

    async def find_all_by_filters(
            self,
            filters: dict = None,
            order: str = 'id',
            desc: bool = False
    ) -> List[ModelType]:
        """Not Implemented"""

    async def create(self, obj_in: Union[CreateSchemaType, Dict[str, Any]]) -> ModelType:
        """Not Implemented"""

    async def update(
        self,
        db_obj: ModelType,
        obj_in: Union[UpdateSchemaType, Dict[str, Any]]
    ) -> ModelType:
        """Not Implemented"""

    async def delete(self, obj: ModelType):
        """Not Implemented"""

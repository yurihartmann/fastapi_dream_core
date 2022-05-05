from abc import ABC
from contextlib import AbstractContextManager
from typing import Generic, Type, Any, Optional, Dict, Union, List, Callable

from fastapi.encoders import jsonable_encoder
from sqlmodel import Session, select, desc as descending, func

from fastapi_dream_core.pagination import PageQuery, Page
from fastapi_dream_core.constants import ModelType, CreateSchemaType, UpdateSchemaType
from fastapi_dream_core.repository.base_repository_abc import BaseRepositoryABC


class BaseRepository(Generic[ModelType, CreateSchemaType, UpdateSchemaType], BaseRepositoryABC, ABC):

    def __init__(self, session_factory: Callable[..., AbstractContextManager[Session]], model: Type[ModelType]):
        '''
        The constructor received the session and the model of repository
        :param session: The session of SQLModel or sqlalchemy
        :param model: The model of repository, example: UserModel, ItemModel
        '''
        self.session_factory = session_factory
        self.model = model

    async def __sanitize_filters_from_model(self, filters: dict) -> dict:
        """
        This method received the filters for query and check if field have in model passed in constructor
        and if do not exists in model remove
        :param filters: A dict with filters, example {'id': 1, 'name': 'foo'}
        :return: return the filters dict with only correct filters
        """
        if not isinstance(filters, dict):
            raise ValueError(f'filters should be a dict, received {type(filters)}')

        keys = list(filters.keys())
        for key in keys:
            try:
                getattr(self.model, key)
            except AttributeError:
                del filters[key]

        return filters

    async def find_one_by_filters(self, filters: Dict[str, Any] = None) -> Optional[ModelType]:
        """
        This method make query using params, filters
        :param filters:
        :return: The object ModelType | None
        """
        with self.session_factory() as session:
            filters = await self.__sanitize_filters_from_model(filters=filters) if filters else {}
            query = select(self.model).filter_by(**filters)

            return session.exec(query).first()

    async def find_by_filters_paginated(
            self,
            page_query: PageQuery = PageQuery(),
            filters: dict = None,
            order: str = 'id',
            desc: bool = False
    ) -> Page:
        """
        This method make query using params, filters, order and desc applied
        :param page_query: The obj Params (page and size)
        :param filters: A dict with filters, example {'id': 1, 'name': 'foo'}
        :param order: The field for ordering select in database
        :param desc: When False the select is using ASC, when True the select is using DESC
        :return: The object PaginationResult(items and count)
                items: The data of select
                count: with count of items for the filters
        """
        if not isinstance(page_query, PageQuery):
            raise ValueError(f'page_query should be a PageQuery obj, received {type(page_query)}')

        with self.session_factory() as session:
            filters = await self.__sanitize_filters_from_model(filters=filters) if filters else {}

            query = select(self.model).filter_by(**filters)

            if hasattr(self.model, order):
                query = query.order_by(descending(order)) if desc else query.order_by(order)

            query = query.offset(page_query.get_offset()).limit(page_query.size)
            count = await self.__count_by_filters_query(filters=filters)

            return Page.create(
                items=session.exec(query).all(),
                total=count,
                page_query=page_query
            )

    async def find_all_by_filters(
            self,
            filters: dict = None,
            order: str = 'id',
            desc: bool = False
    ) -> List[ModelType]:
        """
        This method make query using params, filters, order and desc applied
        :param filters: A dict with filters, example {'id': 1, 'name': 'foo'}
        :param order: The field for ordering select in database
        :param desc: When False the select is using ASC, when True the select is using DESC
        :return: Return a list of Models
        """
        with self.session_factory() as session:
            filters = await self.__sanitize_filters_from_model(filters=filters) if filters else {}
            query = select(self.model).filter_by(**filters)

            if hasattr(self.model, order):
                query = query.order_by(descending(order)) if desc else query.order_by(order)

            return session.exec(query).all()

    async def __count_by_filters_query(self, filters: dict) -> Optional[int]:
        """
        Rerturn count of query
        :param filters:
        :return: int
        """
        with self.session_factory() as session:
            query = select([func.count()]).select_from(self.model).filter_by(**filters)

            result = session.exec(query)
            return result.first()

    async def count_by_filters(
            self,
            filters: dict = None
    ) -> int:
        """
        This method count items with filters
        :param filters: A dict with filters, example {'id': 1, 'name': 'foo'}
        :return: Return int that represent the count of query
        """
        filters = await self.__sanitize_filters_from_model(filters=filters) if filters else {}
        return await self.__count_by_filters_query(filters=filters)

    async def create(self, obj_in: Union[CreateSchemaType, Dict[str, Any]]) -> ModelType:
        """
        This method create object in database
        :param obj_in: The BaseModel with field and data or dict of data
        :return: The Model created
        """
        if isinstance(obj_in, dict):
            new_obj = self.model()

            for field in obj_in:
                if field in obj_in:
                    setattr(new_obj, field, obj_in[field])

        else:
            payload = jsonable_encoder(obj_in)
            new_obj = self.model(**payload)

        with self.session_factory() as session:
            session.add(new_obj)
            session.commit()
            session.refresh(new_obj)
            return new_obj

    async def update(
        self,
        db_obj: ModelType,
        obj_in: Union[UpdateSchemaType, Dict[str, Any]]
    ) -> ModelType:
        """
        This method update the model in database
        :param db_obj: The Model in a database
        :param obj_in: The BaseModel with field and data
        :return: The Model updated
        """
        obj_data = jsonable_encoder(db_obj)
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)

        for field in obj_data:
            if field in update_data:
                setattr(db_obj, field, update_data[field])

        with self.session_factory() as session:
            session.add(db_obj)
            session.commit()
            session.refresh(db_obj)
            return db_obj

    async def delete(self, obj: ModelType):
        """
        This method delete item in database
        :param obj: The Model that will be deleted
        :return: The result of commit
        """
        with self.session_factory() as session:
            session.delete(obj)
            session.commit()

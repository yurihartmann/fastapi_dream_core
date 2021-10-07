from abc import ABC
from typing import Generic, Type, Any, Optional, Dict, Union, List

from fastapi.encoders import jsonable_encoder
from sqlmodel import Session
from sqlalchemy import desc as sql_desc

from fastapi_dream_core import Params, PaginationResult
from fastapi_dream_core.constants import ModelType, CreateSchemaType, UpdateSchemaType


class BaseRepository(Generic[ModelType, CreateSchemaType, UpdateSchemaType], ABC):

    def __init__(self, session: Session, model: Type[ModelType]):
        '''
        The constructor received the session and the model of repository
        :param session: The session of SQLModel or sqlalchemy
        :param model: The model of repository, example: UserModel, ItemModel
        '''
        self.session = session
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

        to_delete = []
        for key in filters.keys():
            try:
                getattr(self.model, key)
            except AttributeError:
                to_delete.append(key)

        for key in to_delete:
            del filters[key]

        return filters

    async def get_one_by_filters(self, filters: Dict[str, Any] = None) -> Optional[ModelType]:
        """
        This method make query using params, filters
        :param filters:
        :return: The object ModelType | None
        """
        filters = await self.__sanitize_filters_from_model(filters=filters) if filters else {}
        return self.session.query(self.model).filter_by(**filters).first()

    async def find_by_filters_paginated(
            self,
            params: Params = Params(),
            filters: dict = None,
            order: str = 'id', # TODO: ver se tem como passar mais de uma ordenação
            desc: bool = False
    ) -> PaginationResult:
        """
        This method make query using params, filters, order and desc applied
        :param params: The obj Params (page and size)
        :param filters: A dict with filters, example {'id': 1, 'name': 'foo'}
        :param order: The field for ordering select in database
        :param desc: When False the select is using ASC, when True the select is using DESC
        :return: The object PaginationResult(items and count)
                items: The data of select
                count: with count of items for the filters
        """
        if not isinstance(params, Params):
            raise ValueError(f'params should be a Params obj, received {type(params)}')

        filters = await self.__sanitize_filters_from_model(filters=filters) if filters else {}

        query = self.session.query(self.model).filter_by(**filters)

        if hasattr(self.model, order):
            query = query.order_by(sql_desc(order)) if desc else query.order_by(order)

        count = query.count()
        query = query.offset(params.get_offset()).limit(params.size)

        return PaginationResult(items=query.all(), count=count)

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
        filters = await self.__sanitize_filters_from_model(filters=filters) if filters else {}

        query = self.session.query(self.model).filter_by(**filters)
        if hasattr(self.model, order):
            query = query.order_by(sql_desc(order)) if desc else query.order_by(order)

        return query.all()

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

        query = self.session.query(self.model).filter_by(**filters)

        return query.count()

    async def create(self, obj_in: CreateSchemaType) -> ModelType:
        """
        This method create object in database
        :param obj_in: The BaseModel with field and data
        :return: The Model created
        """
        payload = jsonable_encoder(obj_in)
        new_obj = self.model(**payload)
        self.session.add(new_obj)
        self.session.commit()
        self.session.refresh(new_obj)
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

        self.session.add(db_obj)
        self.session.commit()
        self.session.refresh(db_obj)
        return db_obj

    async def delete(self, obj: ModelType):
        """
        This method delete item in database
        :param obj: The Model that will be deleted
        :return: The result of commit
        """
        self.session.delete(obj)
        return self.session.commit()

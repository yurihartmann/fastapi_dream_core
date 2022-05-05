from http import HTTPStatus

from fastapi.exceptions import HTTPException
from pydantic import BaseModel


class EntityNotFound(HTTPException):

    def __init__(self):
        super(EntityNotFound, self).__init__(
            status_code=HTTPStatus.NOT_FOUND,
            detail='Entity not found!'
        )


class InternalErrorSchema(BaseModel):
    detail: str = "Internal error."

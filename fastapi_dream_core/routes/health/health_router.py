from http import HTTPStatus

from fastapi import APIRouter
from fastapi.responses import JSONResponse

from fastapi_dream_core.routes.health.health_schemas import AliveSchema, ReadySchema, StatusReadyEnum
from fastapi_dream_core.helpers.readiness import Readiness

health_router = APIRouter()


@health_router.get(
    path='/alive',
    status_code=HTTPStatus.OK,
    response_model=AliveSchema,
    description='This endpoint is check if service still alive'
)
async def health_check():
    return AliveSchema()


@health_router.get(
    path='/ready',
    response_model=ReadySchema,
    description='This endpoint is check if fastapi is ready for connections'
)
async def health_check():
    ready_schema: ReadySchema = ReadySchema(dependencies=Readiness().ready())

    status_code = HTTPStatus.OK
    for dependency in ready_schema.dependencies:
        if not dependency.ready:
            status_code = HTTPStatus.BAD_REQUEST
            ready_schema.status = StatusReadyEnum.NOT_OK.value
            break

    return JSONResponse(status_code=status_code, content=ready_schema.dict())

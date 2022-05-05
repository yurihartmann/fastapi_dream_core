import traceback
from http import HTTPStatus

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import JSONResponse

from fastapi_dream_core.exceptions import InternalErrorSchema
from fastapi_dream_core.utils import logger


class AppMiddleware(BaseHTTPMiddleware):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    async def dispatch(self, request: Request, call_next):
        try:
            response = await call_next(request)
            return response

        except Exception:
            logger.error(traceback.format_exc())

            response = JSONResponse(
                status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
                content=InternalErrorSchema().dict()
            )
            return response

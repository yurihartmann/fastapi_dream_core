import time

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request

from fastapi_dream_core.utils import logger


class DevelopMiddleware(BaseHTTPMiddleware):
    def __init__(self, is_environment_dev: bool = False, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.is_environment_dev = is_environment_dev

    async def dispatch(self, request: Request, call_next):
        if not self.is_environment_dev:
            return await call_next(request)

        start_time = time.perf_counter()

        response = await call_next(request)

        process_time = time.perf_counter() - start_time
        logger.info("Request completed in {0:.5f}ms".format(process_time))

        response.headers["X-Process-Time"] = str(process_time)
        return response

from typing import List

from fastapi import FastAPI, APIRouter
from starlette.middleware.cors import CORSMiddleware
from dependency_injector.containers import Container

from fastapi_dream_core.application_dependencies.application_dependencies_abc import ApplicationDependenciesABC
from fastapi_dream_core.exceptions import InternalErrorSchema
from fastapi_dream_core.middleware import DevelopMiddleware
from fastapi_dream_core.middleware.app_middleware import AppMiddleware
from fastapi_dream_core.routes.health.health_router import health_router
from fastapi_dream_core.routes.migrations.run_migrations_router import run_migrations_router
from fastapi_dream_core.helpers.readiness import Readiness
from fastapi_dream_core.environments import AppBaseEnvironments


def fast_api_create_app(
        app_router: APIRouter,
        version: str = '0.1.0',
        container: Container = None,
        dependencies: List[ApplicationDependenciesABC] = None,
        migration_route_include_in_app: bool = True,
) -> FastAPI:
    # Create FastAPI
    app = FastAPI(
        title=AppBaseEnvironments.APP_TITLE,
        version=version,
        openapi_url=f"{AppBaseEnvironments.BASE_PATH}/openapi.json",
        docs_url=f"{AppBaseEnvironments.BASE_PATH}/docs",
        redoc_url=f"{AppBaseEnvironments.BASE_PATH}/redoc"
    )

    # Allow CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=['*'],
        allow_credentials=True,
        allow_methods=['*'],
        allow_headers=['*'],
    )

    # Add DevelopMiddleware
    app.add_middleware(
        DevelopMiddleware,
        is_environment_dev=AppBaseEnvironments().is_dev_environment()
    )

    # Add AppMiddleware
    app.add_middleware(
        AppMiddleware
    )

    app_router.include_router(
        router=health_router,
        prefix='/health',
        tags=['health']
    )

    if migration_route_include_in_app:
        app_router.include_router(
            router=run_migrations_router,
            prefix='/migrations',
            tags=['migrations']
        )

    # include app_router with response and base path
    app.include_router(
        router=app_router,
        prefix=AppBaseEnvironments.BASE_PATH,
        responses={
            500: {
                'model': InternalErrorSchema
            }
        }
    )

    # Create redirect from '/' from '..../docs'
    if AppBaseEnvironments().is_dev_environment():
        # Add redirect to docs
        from starlette.responses import RedirectResponse

        @app.get("/", response_class=RedirectResponse, include_in_schema=False)
        async def redirect_fastapi():
            return app.docs_url

    # Add container in app
    if container:
        app.container = container

    # Register dependencies
    readiness_service = Readiness()
    for dependency in (dependencies if dependencies else []):
        readiness_service.add_dependency(dependency)

    return app

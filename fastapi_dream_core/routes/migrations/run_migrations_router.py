import os

from fastapi import APIRouter

from fastapi_dream_core.routes.migrations.run_migrations_schemas import RunMigrationsSchema, MIGRATION_ERROR, \
    MIGRATION_SUCCESS

run_migrations_router = APIRouter()

COMMAND = 'alembic upgrade head'


@run_migrations_router.get(
    path='/run',
    response_model=RunMigrationsSchema,
    description=f'This route execute the command in terminal | COMMAND: "{COMMAND}"'
)
async def run_migrations():
    # Run migrations
    result = os.system(COMMAND)

    if os.WEXITSTATUS(result) > 0:
        return RunMigrationsSchema(message=MIGRATION_ERROR)
    else:
        return RunMigrationsSchema(message=MIGRATION_SUCCESS)


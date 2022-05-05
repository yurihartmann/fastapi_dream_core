from pydantic import BaseModel

MIGRATION_SUCCESS = 'Success in run migrations'
MIGRATION_ERROR = 'Error in run migrations - See more details in logs of services'


class RunMigrationsSchema(BaseModel):
    message: str

import os


class AppBaseEnvironments:

    ENVIRONMENT: str = os.getenv('ENVIRONMENT', default='DEV')
    BASE_PATH: str = os.getenv('BASE_PATH', default='')
    APP_TITLE: str = os.getenv('APP_TITLE', default='FastAPI Dream Core')
    APP_HOST: str = os.getenv('APP_HOST', default="127.0.0.1")
    APP_PORT: int = os.getenv('APP_PORT', default=8000)

    def is_dev_environment(self) -> bool:
        return True if self.ENVIRONMENT.upper() == 'DEV' else False

    def is_hml_environment(self) -> bool:
        return True if self.ENVIRONMENT.upper() == 'HML' else False

    def is_prd_environment(self) -> bool:
        return True if self.ENVIRONMENT.upper() == 'PRD' else False

    def get_boto3_by_environment(self):
        if self.is_dev_environment():
            import localstack_client.session as boto3
            return boto3

        import boto3
        return boto3


class CacheEnvironments:
    REDIS_HOST = os.getenv('REDIS_HOST', default='localhost')
    REDIS_PORT = os.getenv('REDIS_PORT', default=6379)
    REDIS_PASSWORD = os.getenv('REDIS_PASSWORD', default=None)


class DatabaseEnvironments:
    DB_URL = os.getenv('DB_URL', default=None)

    DB_HOST = os.getenv('DB_HOST', default='localhost')
    DB_USER = os.getenv('DB_USER', default='root')
    DB_PASSWORD = os.getenv('DB_PASSWORD', default='')
    DB_NAME = os.getenv('DB_NAME', default='')
    DB_PORT = os.getenv('DB_PORT', default=3306)

    def get_db_url(self):
        if self.DB_URL:
            return self.DB_URL

        return f"mysql://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"


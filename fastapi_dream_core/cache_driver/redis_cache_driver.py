import redis

from typing import Union

from fastapi_dream_core.cache_driver import CacheDriverABC
from fastapi_dream_core.environments import CacheEnvironments
from fastapi_dream_core.utils import logger


class RedisCacheDriver(CacheDriverABC):

    def __init__(self):
        host: str = CacheEnvironments.REDIS_HOST
        port: int = CacheEnvironments.REDIS_PORT
        password: str = CacheEnvironments.REDIS_PASSWORD

        is_ssl = password is not None
        self.redis = redis.Redis(
            host=host,
            port=port,
            password=password,
            ssl=is_ssl
        )

    def get(self, key: str) -> Union[bytes, None]:
        try:
            return self.redis.get(name=key)
        except Exception as exc:
            logger.error(f'Error in RedisCacheDriver - Error in get value for key={key} - Exception = {exc}')
            return None

    def set(self, key: str, value, seconds_for_expire: int = 600):
        try:
            self.redis.set(name=key, value=value, ex=seconds_for_expire)
        except Exception as exc:
            logger.error(f'Error in RedisCacheDriver - Error in set key={key} - Exception = {exc}')

    def dump(self, key: str):
        try:
            self.redis.delete(key)
        except Exception as exc:
            logger.error(f'Error in RedisCacheDriver - Error in dump value for key={key} - Exception = {exc}')

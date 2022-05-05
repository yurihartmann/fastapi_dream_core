import dataclasses
from typing import Union

import datetime

from fastapi_dream_core.cache_driver import CacheDriverABC


@dataclasses.dataclass
class CacheData:
    value: bytes
    seconds_for_expire: int
    datetime: datetime


class InMemoryCacheDriver(CacheDriverABC):

    _memory: dict = {}

    def get(self, key: str) -> Union[bytes, None]:
        cache_data: CacheData = self._memory.get(key)

        if not cache_data:
            return None

        if ((cache_data.datetime - datetime.datetime.now()).total_seconds() * -1) > cache_data.seconds_for_expire:
            del self._memory[key]
            return None

        return cache_data.value

    def set(self, key: str, value, seconds_for_expire: int = 600) -> None:
        self._memory.update({
            key: CacheData(
                value=str(value).encode(),
                seconds_for_expire=seconds_for_expire,
                datetime=datetime.datetime.now()
            )
        })

    def dump(self, key: str) -> None:
        if self._memory.get(key):
            del self._memory[key]

        return None

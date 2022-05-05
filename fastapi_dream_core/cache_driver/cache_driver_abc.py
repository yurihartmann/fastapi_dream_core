from abc import ABC
from typing import Union


class CacheDriverABC(ABC):

    def get(self, key: str) -> Union[bytes, None]:
        """Not Implemented"""

    def set(self, key: str, value, seconds_for_expire: int = 600) -> None:
        """Not Implemented"""

    def dump(self, key: str) -> None:
        """Not Implemented"""

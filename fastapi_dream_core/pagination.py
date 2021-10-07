from abc import ABC, abstractmethod
from functools import wraps
from typing import TypeVar, Generic, Sequence, Any, List, ClassVar, Type, cast, Dict, Mapping
from collections import ChainMap

from fastapi import Query
from pydantic import BaseModel, conint, create_model
from pydantic.generics import GenericModel

from fastapi_dream_core.constants import ModelType

T = TypeVar("T")
C = TypeVar("C")

TAbstractPage = TypeVar("TAbstractPage", bound="AbstractPage")


class Params(BaseModel):
    page: int = Query(1, ge=1, description="Page number")
    size: int = Query(20, ge=1, description="Page size")

    def get_offset(self):
        return (self.page - 1) * self.size


def _create_params(cls: Type[Params], fields: Dict[str, Any]) -> Mapping[str, Any]:
    if not issubclass(cls, BaseModel):
        raise ValueError(f"{cls.__name__} must be subclass of BaseModel")

    incorrect = sorted(fields.keys() - cls.__fields__.keys())
    if incorrect:
        ending = "s" if len(incorrect) > 1 else ""
        raise ValueError(f"Unknown field{ending} {', '.join(incorrect)}")

    anns = ChainMap(*(obj.__dict__.get("__annotations__", {}) for obj in cls.mro()))
    return {name: (anns[name], val) for name, val in fields.items()}


class AbstractPage(GenericModel, Generic[T], ABC):
    __params_type__: ClassVar[Type[Params]]

    @classmethod
    @abstractmethod
    def create(cls: Type[C], items: Sequence[T], total: int, params: Params) -> C:
        pass

    @classmethod
    def with_custom_options(cls: Type[TAbstractPage], **kwargs: Any) -> Type[TAbstractPage]:
        params_cls = cast(Type[AbstractPage], cls).__params_type__

        custom_params: Any = create_model(
            params_cls.__name__,
            __base__=params_cls,
            **_create_params(params_cls, kwargs),
        )

        if cls.__concrete__:
            bases = (cls,)
        else:
            bases = (cls[T], Generic[T])  # type: ignore

        @wraps(cls, updated=())
        class CustomPage(*bases):  # type: ignore
            __params_type__: ClassVar[Type[Params]] = custom_params

        return cast(Type[TAbstractPage], CustomPage)

    class Config:
        arbitrary_types_allowed = True


class PaginationResult(BaseModel):
    items: List[ModelType]
    count: int


class Page(AbstractPage, Generic[T]):
    page: conint(ge=1)
    size: conint(ge=1)
    total: conint(ge=0)
    items: Sequence[T]

    @classmethod
    def create(cls, items: Sequence[T], total: int, params):
        return cls(
            total=total,
            items=items,
            page=params.page,
            size=params.size
        )

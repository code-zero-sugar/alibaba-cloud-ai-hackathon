from typing import Generic, Type, TypeVar
from pydantic import BaseModel

T = TypeVar("T")


class BaseDto(BaseModel, Generic[T]):
    _orm_model: Type[T]

    def to_orm(self) -> T:
        return self._orm_model(**self.model_dump())

    @classmethod
    def from_orm(cls, orm_model: T):
        return cls(**orm_model.__dict__)

from typing import Generic, Optional, TypeVar
from uuid import uuid4

_T = TypeVar("_T")


class Entity(Generic[_T]):
    __id: str
    __data: _T

    @classmethod
    def create(cls, data: _T, id: Optional[str] = None) -> "Entity[_T]":
        entity = cls()
        entity.__id = id if id != None else str(uuid4())
        entity.__data = data
        return entity

    @property
    def id(self) -> str:
        return self.__id

    @property
    def data(self) -> _T:
        return self.__data

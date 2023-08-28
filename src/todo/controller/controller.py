from abc import ABC, abstractmethod
from typing import Generic, TypeVar

_T = TypeVar("_T")
_R = TypeVar("_R")


class Controller(ABC, Generic[_T, _R]):
    @abstractmethod
    async def perform(self, request: _T) -> _R:
        ...

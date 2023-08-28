from abc import ABC, abstractmethod
from collections.abc import Sequence
from typing import Generic, Optional, TypeVar

from ..entity import Entity

_T = TypeVar("_T")


class Repository(ABC, Generic[_T]):
    @abstractmethod
    async def save(self, entity: Entity[_T]) -> None:
        ...

    @abstractmethod
    async def remove(self, id: str) -> Optional[Entity[_T]]:
        ...

    @abstractmethod
    async def get_by_id(self, id: str) -> Optional[Entity[_T]]:
        ...

    @abstractmethod
    async def get_all(self) -> Sequence[Entity[_T]]:
        ...

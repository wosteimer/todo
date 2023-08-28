from collections.abc import Sequence
from typing import Dict, Optional

from ..entity import Entity, Todo
from .repository import Repository


class InMemoryTodoRepository(Repository[Todo]):
    __data: Dict[str, Todo]

    @classmethod
    def create(cls) -> "InMemoryTodoRepository":
        repo = cls()
        repo.__data = {}
        return repo

    async def save(self, entity: Entity[Todo]) -> None:
        self.__data[entity.id] = entity.data

    async def remove(self, id: str) -> Optional[Entity[Todo]]:
        if id in self.__data:
            return Entity.create(self.__data.pop(id), id=id)

    async def get_by_id(self, id: str) -> Optional[Entity[Todo]]:
        if id in self.__data:
            return Entity.create(self.__data[id], id=id)

    async def get_all(self) -> Sequence[Entity[Todo]]:
        entities = (Entity.create(todo, id=id) for id, todo in self.__data.items())
        return tuple(entities)

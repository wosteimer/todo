from __future__ import annotations
from abc import ABC, abstractmethod
from collections.abc import Sequence
from todo.entity.todo import Todo
from uuid import UUID

type Result[T, E: Exception] = tuple[T, E | None]


class TodoNotFoundError(Exception): ...


class TodoRepository(ABC):
    @abstractmethod
    async def save(self, todo: Todo) -> None: ...
    @abstractmethod
    async def delete(self, id: UUID) -> Result[Todo, TodoNotFoundError]: ...
    @abstractmethod
    async def get(self, id: UUID) -> Result[Todo, TodoNotFoundError]: ...
    @abstractmethod
    async def get_all(self) -> Sequence[Todo]: ...

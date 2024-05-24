from __future__ import annotations

from abc import ABC, abstractmethod
from collections.abc import Sequence
from uuid import UUID

from returns import Result

from todo.entity.todo import Todo

from ..errors import TodoNotFoundError


class TodoRepository(ABC):
    @abstractmethod
    async def save(self, todo: Todo) -> None: ...
    @abstractmethod
    async def delete(self, id: UUID) -> Result[Todo, TodoNotFoundError]: ...
    @abstractmethod
    async def get(self, id: UUID) -> Result[Todo, TodoNotFoundError]: ...
    @abstractmethod
    async def get_all(self) -> Sequence[Todo]: ...

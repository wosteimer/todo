from collections.abc import Sequence
from typing import override
from uuid import UUID

from returns import Err, Ok, Result

from ..entity.todo import Todo
from ..errors import TodoNotFoundError
from .todo_repository import TodoRepository


class InMemoryTodoRepository(TodoRepository):
    def __init__(self) -> None:
        self.__data = dict[UUID, Todo]()

    @override
    async def save(self, todo: Todo) -> None:
        self.__data[todo.id] = todo

    @override
    async def delete(self, id: UUID) -> Result[Todo, TodoNotFoundError]:
        if id not in self.__data:
            return Err(TodoNotFoundError())
        return Ok(self.__data.pop(id))

    @override
    async def get(self, id: UUID) -> Result[Todo, TodoNotFoundError]:
        if id not in self.__data:
            return Err(TodoNotFoundError())
        return Ok(self.__data[id])

    @override
    async def get_all(self) -> Sequence[Todo]:
        return tuple(self.__data.values())

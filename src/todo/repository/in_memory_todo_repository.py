from collections.abc import Sequence
from datetime import datetime
from typing import override
from uuid import UUID

from todo.entity.todo import Todo
from todo.repository.todo_repository import Result, TodoNotFoundError, TodoRepository


class InMemoryTodoRepository(TodoRepository):
    def __init__(self) -> None:
        self.__data = dict[UUID, Todo]()

    @override
    async def save(self, todo: Todo) -> None:
        self.__data[todo.id] = todo

    @override
    async def delete(self, id: UUID) -> Result[Todo, TodoNotFoundError]:
        if id not in self.__data:
            return (
                Todo(
                    UUID("00000000-0000-0000-0000-000000000000"),
                    "",
                    False,
                    datetime(year=1, month=1, day=1),
                    datetime(year=1, month=1, day=1),
                ),
                TodoNotFoundError(),
            )
        return self.__data.pop(id), None

    @override
    async def get(self, id: UUID) -> Result[Todo, TodoNotFoundError]:
        if id not in self.__data:
            return (
                Todo(
                    UUID("00000000-0000-0000-0000-000000000000"),
                    "",
                    False,
                    datetime(year=1, month=1, day=1),
                    datetime(year=1, month=1, day=1),
                ),
                TodoNotFoundError(),
            )
        return self.__data[id], None

    @override
    async def get_all(self) -> Sequence[Todo]:
        return tuple(self.__data.values())

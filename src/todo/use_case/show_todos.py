from collections.abc import Sequence
from typing import TypedDict
from uuid import UUID

from ..repository.todo_repository import TodoRepository


class Output(TypedDict):
    id: UUID
    content: str
    its_done: bool


class ShowTodos:
    def __init__(self, todos: TodoRepository) -> None:
        self.__todos = todos

    async def perform(self) -> Sequence[Output]:
        todos = await self.__todos.get_all()
        return [
            {"id": todo.id, "content": todo.content, "its_done": todo.its_done}
            for todo in todos
        ]

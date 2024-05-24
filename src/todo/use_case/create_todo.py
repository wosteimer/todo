import asyncio
from typing import TypedDict, Unpack
from uuid import UUID

from returns import Err, Ok, Result

from ..entity.todo import InvalidContentError, Todo
from ..repository.todo_repository import TodoRepository


class Input(TypedDict):
    content: str


class Output(TypedDict):
    id: UUID
    content: str
    its_done: bool


class CreateTodo:
    def __init__(self, todos: TodoRepository) -> None:
        self.__todos = todos

    async def perform(
        self, **input: Unpack[Input]
    ) -> Result[Output, InvalidContentError]:
        content = input["content"]
        result = Todo.create(content)
        # fmt:off
        match result:
            case Err(err): return Err(err)
            case Ok(todo):
                asyncio.create_task(self.__todos.save(todo))
                return Ok({"id": todo.id, "content": todo.content, "its_done": todo.its_done})
        # fmt:on

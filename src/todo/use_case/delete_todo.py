from typing import TypedDict, Unpack
from uuid import UUID

from returns import Err, Ok, Result

from ..errors import TodoNotFoundError
from ..repository.todo_repository import TodoRepository


class Input(TypedDict):
    id: UUID


class Output(TypedDict):
    id: UUID
    content: str
    its_done: bool


class DeleteTodo:
    def __init__(self, todos: TodoRepository):
        self.__todos = todos

    async def perform(
        self, **input: Unpack[Input]
    ) -> Result[Output, TodoNotFoundError]:
        id = input["id"]
        result = await self.__todos.delete(id)
        # fmt: off
        match result:
            case Ok(todo): return Ok({"id": todo.id, "content": todo.content, "its_done": todo.its_done})
            case Err(err): return Err(err) 
        # fmt: on

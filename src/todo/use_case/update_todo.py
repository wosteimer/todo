import asyncio
from typing import Required, TypedDict, Unpack
from uuid import UUID

from returns import Err, Ok, Result

from todo.repository.todo_repository import TodoRepository

from ..errors import InvalidContentError, TodoNotFoundError


class Input(TypedDict, total=False):
    id: Required[UUID]
    content: str
    its_done: bool


class Output(TypedDict):
    id: UUID
    content: str
    its_done: bool


class UpdateTodo:
    def __init__(self, todos: TodoRepository) -> None:
        self.__todos = todos

    async def perform(
        self, **input: Unpack[Input]
    ) -> Result[Output, TodoNotFoundError | InvalidContentError]:
        id = input["id"]
        result = await self.__todos.get(id)
        # fmt: off
        match result:
            case Err(err): return Err(err)
            case Ok(todo): 
                content, its_done = input.get("content", todo.content), input.get("its_done", todo.its_done),
                result = todo.update(content=content, its_done=its_done)
                if result.is_err():
                    return Err(InvalidContentError())
                updated_todo = result.unwrap()
                asyncio.create_task(self.__todos.save(updated_todo))
                return Ok({
                    "id": updated_todo.id,
                    "content": updated_todo.content,
                    "its_done": updated_todo.its_done,
                })
        # fmt: on

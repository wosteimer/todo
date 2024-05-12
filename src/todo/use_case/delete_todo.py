from typing import TypedDict, Unpack
from uuid import UUID

from ..repository.todo_repository import TodoRepository, TodoNotFoundError


class Input(TypedDict):
    id: UUID


class Output(TypedDict):
    id: UUID
    content: str
    its_done: bool


type = Result = tuple[Output, TodoNotFoundError | None]


class DeleteTodo:
    def __init__(self, todos: TodoRepository):
        self.__todos = todos

    async def perform(self, **input: Unpack[Input]) -> Result:
        id = input["id"]
        todo, err = await self.__todos.delete(id)
        if err != None:
            return {
                "id": UUID("00000000-0000-0000-0000-000000000000"),
                "content": "",
                "its_done": False,
            }, err
        return {"id": todo.id, "content": todo.content, "its_done": todo.its_done}, err

from typing import Required, TypedDict, Unpack
from uuid import UUID

from todo.repository.todo_repository import TodoNotFoundError, TodoRepository


class Input(TypedDict, total=False):
    id: Required[UUID]
    content: str
    its_done: bool


class Output(TypedDict):
    id: UUID
    content: str
    its_done: bool


type Result = tuple[Output, TodoNotFoundError | None]


class UpdateTodo:
    def __init__(self, todos: TodoRepository) -> None:
        self.__todos = todos

    async def perform(self, **input: Unpack[Input]) -> Result:
        id = input["id"]
        todo, err = await self.__todos.get(id)
        if err != None:
            return {
                "id": UUID("00000000-0000-0000-0000-000000000000"),
                "content": "",
                "its_done": False,
            }, err
        content, its_done = (
            input.get("content", todo.content),
            input.get("its_done", todo.its_done),
        )
        updated_todo = todo.update(content=content, its_done=its_done)
        await self.__todos.save(updated_todo)
        return {
            "id": updated_todo.id,
            "content": updated_todo.content,
            "its_done": updated_todo.its_done,
        }, None

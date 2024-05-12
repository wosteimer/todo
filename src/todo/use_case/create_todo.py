from typing import TypedDict, Unpack
from uuid import UUID

from ..repository.todo_repository import TodoRepository

from ..entity import Todo


class Input(TypedDict):
    content: str


class Output(TypedDict):
    id: UUID
    content: str
    its_done: bool


class CreateTodo:
    def __init__(self, todos: TodoRepository) -> None:
        self.__todos = todos

    async def perform(self, **input: Unpack[Input]) -> Output:
        content = input["content"]
        todo = Todo.create(content)
        await self.__todos.save(todo)

        return {"id": todo.id, "content": todo.content, "its_done": todo.its_done}

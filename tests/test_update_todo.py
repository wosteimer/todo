from uuid import uuid4
import pytest

from todo.entity.todo import Todo
from todo.repository.in_memory_todo_repository import InMemoryTodoRepository
from todo.repository.todo_repository import TodoNotFoundError
from todo.use_case.update_todo import Input, UpdateTodo


@pytest.mark.asyncio
async def test_case_1():
    """It is expected that it will be possible to update a todo"""
    todos = InMemoryTodoRepository()
    todo = Todo.create("Test Todo")
    await todos.save(todo)
    input: Input = {"id": todo.id, "content": "Test Todo 1", "its_done": True}
    case = UpdateTodo(todos)
    output, err = await case.perform(**input)
    assert err == None
    assert output["id"] == input["id"]
    assert output["content"] == input["content"]
    assert output["its_done"] == input["its_done"]


@pytest.mark.asyncio
async def test_case_2():
    """an error is expected if the todo does not exist"""
    todos = InMemoryTodoRepository()
    input: Input = {"id": uuid4(), "content": "Test Todo", "its_done": True}
    case = UpdateTodo(todos)
    _, err = await case.perform(**input)
    assert isinstance(err, TodoNotFoundError)

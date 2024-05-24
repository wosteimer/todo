from uuid import uuid4

import pytest

from todo.entity.todo import Todo
from todo.errors import TodoNotFoundError
from todo.repository.in_memory_todo_repository import InMemoryTodoRepository
from todo.use_case.update_todo import Input, UpdateTodo


@pytest.mark.asyncio
async def test_case_1():
    """It is expected that it will be possible to update a content of todo"""
    todos = InMemoryTodoRepository()
    todo = Todo.create("Test Todo").unwrap()
    await todos.save(todo)
    input: Input = {"id": todo.id, "content": "Test Todo 1"}
    case = UpdateTodo(todos)
    result = await case.perform(**input)
    output = result.unwrap()
    assert output["id"] == input["id"]
    assert output["content"] == input["content"]


@pytest.mark.asyncio
async def test_case_2():
    """It is expected that it will be possible to change its_done property to True"""
    todos = InMemoryTodoRepository()
    todo = Todo.create("Test Todo").unwrap()
    await todos.save(todo)
    input: Input = {"id": todo.id, "its_done": True}
    case = UpdateTodo(todos)
    result = await case.perform(**input)
    output = result.unwrap()
    assert output["id"] == input["id"]
    assert output["its_done"] == input["its_done"]


@pytest.mark.asyncio
async def test_case_3():
    """It is expected that it will be possible to change its_done property to False"""
    todos = InMemoryTodoRepository()
    todo = Todo.create("Test Todo").unwrap()
    todo = todo.update(its_done=True).unwrap()
    await todos.save(todo)
    input: Input = {"id": todo.id, "its_done": False}
    case = UpdateTodo(todos)
    result = await case.perform(**input)
    output = result.unwrap()
    assert output["id"] == input["id"]
    assert output["its_done"] == input["its_done"]


@pytest.mark.asyncio
async def test_case_4():
    """an error is expected if the todo does not exist"""
    todos = InMemoryTodoRepository()
    input: Input = {"id": uuid4(), "content": "Test Todo", "its_done": True}
    case = UpdateTodo(todos)
    result = await case.perform(**input)
    assert isinstance(result.unwrap_err(), TodoNotFoundError)

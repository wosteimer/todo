from uuid import uuid4

import pytest

from todo.entity.todo import Todo
from todo.errors import TodoNotFoundError
from todo.repository.in_memory_todo_repository import InMemoryTodoRepository
from todo.use_case.delete_todo import DeleteTodo


@pytest.mark.asyncio
async def test_case_1():
    """It must be possible to delete a todo"""
    todos = InMemoryTodoRepository()
    todo = Todo.create("Todo Test").unwrap()
    await todos.save(todo)
    case = DeleteTodo(todos)
    input = todo.id
    result = await case.perform(id=input)
    assert result.is_ok()
    output = result.unwrap()
    assert output["id"] == todo.id
    assert output["content"] == todo.content
    assert output["its_done"] == todo.its_done
    result = await todos.get(todo.id)
    assert result.is_err()
    assert isinstance(result.unwrap_err(), TodoNotFoundError)


@pytest.mark.asyncio
async def test_case_2():
    """There must be an error if the todo does not exists"""
    todos = InMemoryTodoRepository()
    case = DeleteTodo(todos)
    input = uuid4()
    result = await case.perform(id=input)
    assert isinstance(result.unwrap_err(), TodoNotFoundError)

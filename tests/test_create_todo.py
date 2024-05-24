import pytest

from todo.repository.in_memory_todo_repository import InMemoryTodoRepository
from todo.use_case.create_todo import CreateTodo


@pytest.mark.asyncio
async def test_case_1():
    """It is expected that it will be possible to create a new todo"""
    todos = InMemoryTodoRepository()
    case = CreateTodo(todos)
    input = {"content": "Todo Test"}
    result = await case.perform(**input)
    output = result.unwrap()

    assert "id" in output
    assert "content" in output
    assert "its_done" in output

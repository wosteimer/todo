import pytest

from todo.entity.todo import Todo
from todo.repository.in_memory_todo_repository import InMemoryTodoRepository
from todo.use_case.show_todos import ShowTodos


@pytest.mark.asyncio
async def test_case_1():
    """It must be possible to get all todos"""
    todos = InMemoryTodoRepository()
    for i in range(3):
        todo = Todo.create(f"Test Todo {i}")
        await todos.save(todo)
    case = ShowTodos(todos)
    output = await case.perform()
    assert len(output) == 3
    assert output[0]["content"] == "Test Todo 0"
    assert output[1]["content"] == "Test Todo 1"
    assert output[2]["content"] == "Test Todo 2"

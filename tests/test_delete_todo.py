import pytest

from uuid import uuid4
from todo.entity.todo import Todo
from todo.repository.in_memory_todo_repository import InMemoryTodoRepository
from todo.repository.todo_repository import TodoNotFoundError
from todo.use_case.delete_todo import DeleteTodo


@pytest.mark.asyncio
async def test_case_1():
    """It must be possible to delete a todo"""
    todos = InMemoryTodoRepository()
    todo = Todo.create("Todo Test")
    await todos.save(todo)
    case = DeleteTodo(todos)
    input = todo.id
    output, err = await case.perform(id=input)
    assert err == None
    assert output["id"] == todo.id
    assert output["content"] == todo.content
    assert output["its_done"] == todo.its_done
    _, err = await todos.get(todo.id)
    assert isinstance(err, TodoNotFoundError)


@pytest.mark.asyncio
async def test_case_2():
    """There must be an error if the todo does not exists"""
    todos = InMemoryTodoRepository()
    case = DeleteTodo(todos)
    input = uuid4()
    _, err = await case.perform(id=input)
    assert isinstance(err, TodoNotFoundError)

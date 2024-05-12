from pathlib import Path
from uuid import uuid4
import pytest
import aiosqlite
from todo.entity.todo import Todo
from todo.repository.sqlite_todo_repository import SqliteTodoRepository
import asyncio

from todo.repository.todo_repository import TodoNotFoundError

DB_PATH = Path("/tmp/test.db")


async def create_db():
    async with aiosqlite.connect(DB_PATH) as connection:
        await connection.execute(
            "CREATE TABLE todo(\n"
            "   id UUID NOT NULL,\n"
            "   content VARCHAR(24) NOT NULL,\n"
            "   its_done BOOLEAN NOT NULL,\n"
            "   created_at TEXT NOT NULL,\n"
            "   updated_at TEXT NOT NULL,\n"
            "   UNIQUE(id),\n"
            "   PRIMARY KEY (id)\n"
            ");\n"
        )
        await connection.commit()


@pytest.fixture
def repository():
    asyncio.run(create_db())
    yield SqliteTodoRepository(DB_PATH)
    DB_PATH.unlink()


@pytest.mark.asyncio
async def test_case_1(repository: SqliteTodoRepository):
    """It is expected that it will be possible to create a new todo"""
    input = Todo.create("Test Todo")
    await repository.save(input)


@pytest.mark.asyncio
async def test_case_2(repository: SqliteTodoRepository):
    """It is expected that it will be possible to update a todo"""
    input = Todo.create("Test Todo")
    await repository.save(input)
    await repository.save(input.update(content="Test Todo 1", its_done=True))
    output, _ = await repository.get(input.id)
    assert output.content == "Test Todo 1"
    assert output.its_done == True


@pytest.mark.asyncio
async def test_case_3(repository: SqliteTodoRepository):
    """It is expected that it will be possible to remove a todo"""
    todo = Todo.create("Test Todo")
    input = todo.id
    await repository.save(todo)

    _, err = await repository.delete(input)
    assert err == None


@pytest.mark.asyncio
async def test_case_4(repository: SqliteTodoRepository):
    """an error is expected when removing a todo that does not exist"""
    input = uuid4()
    _, err = await repository.delete(input)
    assert isinstance(err, TodoNotFoundError)


@pytest.mark.asyncio
async def test_case_5(repository: SqliteTodoRepository):
    """It is expected that it will be possible to get a todo that exists in the repository"""
    todo = Todo.create("Test Todo")
    input = todo.id
    await repository.save(todo)

    output, err = await repository.get(input)
    assert err == None
    assert output.id == input


@pytest.mark.asyncio
async def test_case_6(repository: SqliteTodoRepository):
    """an error is expected if the whole does not exist"""
    input = uuid4()

    _, err = await repository.get(input)
    assert isinstance(err, TodoNotFoundError)


@pytest.mark.asyncio
async def test_case_7(repository: SqliteTodoRepository):
    """It is expected that it will be possible to retrieve all todos from the repository"""
    for _ in range(10):
        todo = Todo.create("Test Todo")
        await repository.save(todo)

    output = await repository.get_all()
    assert len(output) == 10
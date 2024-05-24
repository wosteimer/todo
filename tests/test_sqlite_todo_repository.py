import asyncio
from pathlib import Path
from uuid import uuid4

import aiosqlite
import pytest

from todo.entity.todo import Todo
from todo.errors import TodoNotFoundError
from todo.repository.sqlite_todo_repository import SqlitePool, SqliteTodoRepository

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


async def drop_db():
    async with aiosqlite.connect(DB_PATH) as connection:
        await connection.execute("DROP TABLE todo;\n")
        await connection.commit()


@pytest.fixture
def repository():
    asyncio.run(create_db())
    pool = SqlitePool()
    asyncio.run(pool.connect(DB_PATH))
    todos = SqliteTodoRepository(pool)
    yield todos
    asyncio.run(pool.close())
    asyncio.run(drop_db())
    DB_PATH.unlink()


@pytest.mark.asyncio
async def test_case_1(repository: SqliteTodoRepository):
    """It is expected that it will be possible to create a new todo"""
    input = Todo.create("Test Todo").unwrap()
    await repository.save(input)
    result = await repository.get(input.id)
    output = result.unwrap()
    assert output.id == input.id
    assert output.content == input.content
    assert output.its_done == input.its_done
    assert output.created_at == input.created_at
    assert output.updated_at == input.updated_at


@pytest.mark.asyncio
async def test_case_2(repository: SqliteTodoRepository):
    """It is expected that it will be possible to update a todo"""
    input = Todo.create("Test Todo").unwrap()
    await repository.save(input)
    await repository.save(input.update(content="Test Todo 1", its_done=True).unwrap())
    result = await repository.get(input.id)
    output = result.unwrap()
    assert output.content == "Test Todo 1"
    assert output.its_done == True


@pytest.mark.asyncio
async def test_case_3(repository: SqliteTodoRepository):
    """It is expected that it will be possible to remove a todo"""
    todo = Todo.create("Test Todo").unwrap()
    input = todo.id
    await repository.save(todo)
    result = await repository.delete(input)
    assert result.is_ok()


@pytest.mark.asyncio
async def test_case_4(repository: SqliteTodoRepository):
    """an error is expected when removing a todo that does not exist"""
    input = uuid4()
    result = await repository.delete(input)
    assert isinstance(result.unwrap_err(), TodoNotFoundError)


@pytest.mark.asyncio
async def test_case_5(repository: SqliteTodoRepository):
    """It is expected that it will be possible to get a todo that exists in the repository"""
    todo = Todo.create("Test Todo").unwrap()
    input = todo.id
    await repository.save(todo)
    result = await repository.get(input)
    output = result.unwrap()
    assert output.id == input


@pytest.mark.asyncio
async def test_case_6(repository: SqliteTodoRepository):
    """an error is expected if the whole does not exist"""
    input = uuid4()
    result = await repository.get(input)
    assert isinstance(result.unwrap_err(), TodoNotFoundError)


@pytest.mark.asyncio
async def test_case_7(repository: SqliteTodoRepository):
    """It is expected that it will be possible to retrieve all todos from the repository"""
    for _ in range(10):
        todo = Todo.create("Test Todo").unwrap()
        await repository.save(todo)
    output = await repository.get_all()
    assert len(output) == 10

from asyncio import Queue
from collections.abc import Sequence
from datetime import datetime
from pathlib import Path
from typing import override
from uuid import UUID

import aiosqlite
from returns import Err, Ok, Result

from ..entity.todo import Todo
from ..errors import TodoNotFoundError
from .todo_repository import TodoRepository


class SqlitePool:
    def __init__(self, pool_size: int = 10) -> None:
        self.__pool_size = pool_size
        self.__queue = Queue[aiosqlite.Connection](maxsize=pool_size)

    async def connect(self, db_path: Path | str) -> None:
        for _ in range(self.__pool_size):
            await self.__queue.put(await aiosqlite.connect(db_path))

    async def close(self) -> None:
        for _ in range(self.__pool_size):
            connection = await self.__queue.get()
            await connection.close()
            self.__queue.task_done()
        await self.__queue.join()

    async def get(self) -> aiosqlite.Connection:
        return await self.__queue.get()

    async def put(self, connection: aiosqlite.Connection):
        self.__queue.task_done()
        await self.__queue.put(connection)


class SqliteTodoRepository(TodoRepository):
    def __init__(self, pool: SqlitePool) -> None:
        self.__pool = pool

    @override
    async def save(self, todo: Todo) -> None:
        db = await self.__pool.get()
        query = (
            "INSERT OR REPLACE INTO todo\n"
            "VALUES(:id, :content, :its_done, :created_at, :updated_at);\n"
        )
        parameters = {
            "id": str(todo.id),
            "content": todo.content,
            "its_done": todo.its_done,
            "updated_at": todo.updated_at.isoformat(),
            "created_at": todo.created_at.isoformat(),
        }
        await db.execute(query, parameters)
        await db.commit()
        await self.__pool.put(db)

    @override
    async def delete(self, id: UUID) -> Result[Todo, TodoNotFoundError]:
        db = await self.__pool.get()
        try:
            query = (
                "DELETE FROM todo WHERE id=:id\n"
                "RETURNING content, its_done, created_at, updated_at;\n"
            )
            parameters = {"id": str(id)}
            async with db.execute(query, parameters) as cursor:
                row = await cursor.fetchone()
                if not row:
                    return Err(TodoNotFoundError())
            await db.commit()
            content, its_done, created_at, updated_at = row
            todo = Todo.restore(
                id,
                content,
                bool(its_done),
                datetime.fromisoformat(created_at),
                datetime.fromisoformat(updated_at),
            )
            return Ok(todo)
        finally:
            await self.__pool.put(db)

    @override
    async def get(self, id: UUID) -> Result[Todo, TodoNotFoundError]:
        db = await self.__pool.get()
        try:
            query = "SELECT content, its_done, created_at, updated_at FROM todo WHERE :id=id;\n"
            parameters = {"id": str(id)}
            async with db.execute(query, parameters) as cursor:
                row = await cursor.fetchone()
                if not row:
                    return Err(TodoNotFoundError())
                content, its_done, created_at, updated_at = row
                todo = Todo.restore(
                    id,
                    content,
                    bool(its_done),
                    datetime.fromisoformat(created_at),
                    datetime.fromisoformat(updated_at),
                )
                return Ok(todo)
        finally:
            await self.__pool.put(db)

    @override
    async def get_all(self) -> Sequence[Todo]:
        db = await self.__pool.get()
        # fmt:off
        try:
            query = (
                "SELECT id, content, its_done, created_at, updated_at FROM todo\n"
                "ORDER BY created_at;\n"
            )
            async with db.execute(query) as cursor:
                return tuple([
                    Todo.restore(
                        UUID(id),
                        content,
                        bool(its_done),
                        datetime.fromisoformat(created_at),
                        datetime.fromisoformat(updated_at),
                    )
                    async for id, content, its_done, created_at, updated_at in cursor
                ])
        finally: await self.__pool.put(db)
        # fmt:on

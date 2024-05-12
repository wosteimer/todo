from collections.abc import Sequence
from pathlib import Path
from typing import override
from uuid import UUID
from datetime import datetime
import aiosqlite

from todo.repository.todo_repository import Result, TodoNotFoundError, TodoRepository

from ..entity import Todo


class SqliteTodoRepository(TodoRepository):
    def __init__(self, db_path: Path | str) -> None:
        self.__db_path = db_path

    @override
    async def save(self, todo: Todo) -> None:
        async with aiosqlite.connect(self.__db_path) as db:
            await db.execute(
                "INSERT OR REPLACE INTO todo\n"
                "VALUES(:id, :content, :its_done, :created_at, :updated_at);\n",
                parameters={
                    "id": str(todo.id),
                    "content": todo.content,
                    "its_done": todo.its_done,
                    "updated_at": todo.updated_at.isoformat(),
                    "created_at": todo.created_at.isoformat(),
                },
            )
            await db.commit()

    @override
    async def delete(self, id: UUID) -> Result[Todo, TodoNotFoundError]:
        async with aiosqlite.connect(self.__db_path) as db:
            parameters = {"id": str(id)}
            async with db.execute(
                "DELETE FROM todo WHERE id=:id\n"
                "RETURNING id, content, its_done, created_at, updated_at;\n",
                parameters,
            ) as cursor:
                row = await cursor.fetchone()
                if not row:
                    return (
                        Todo(
                            UUID("00000000-0000-0000-0000-000000000000"),
                            "",
                            False,
                            datetime(year=1, month=1, day=1),
                            datetime(year=1, month=1, day=1),
                        ),
                        TodoNotFoundError(),
                    )
                id, content, its_done, created_at, updated_at = row
                await db.commit()
                return (
                    Todo(
                        UUID(str(id)),
                        content,
                        bool(its_done),
                        datetime.fromisoformat(created_at),
                        datetime.fromisoformat(updated_at),
                    ),
                    None,
                )

    @override
    async def get(self, id: UUID) -> Result[Todo, TodoNotFoundError]:
        async with aiosqlite.connect(self.__db_path) as db:
            parameters = {"id": str(id)}
            async with db.execute(
                "SELECT * FROM todo WHERE :id=id;\n",
                parameters,
            ) as cursor:
                row = await cursor.fetchone()
                if not row:
                    return (
                        Todo(
                            UUID("00000000-0000-0000-0000-000000000000"),
                            "",
                            False,
                            datetime(year=1, month=1, day=1),
                            datetime(year=1, month=1, day=1),
                        ),
                        TodoNotFoundError(),
                    )
                id, content, its_done, created_at, updated_at = row
                return (
                    Todo(
                        UUID(str(id)),
                        content,
                        bool(its_done),
                        datetime.fromisoformat(created_at),
                        datetime.fromisoformat(updated_at),
                    ),
                    None,
                )

    @override
    async def get_all(self) -> Sequence[Todo]:
        result: list[Todo] = []
        async with aiosqlite.connect(self.__db_path) as db:
            async with db.execute(
                "SELECT * FROM todo\n" "ORDER BY created_at;\n",
            ) as cursor:
                async for row in cursor:
                    id, content, its_done, created_at, updated_at = row
                    result.append(
                        Todo(
                            UUID(str(id)),
                            content,
                            bool(its_done),
                            datetime.fromisoformat(created_at),
                            datetime.fromisoformat(updated_at),
                        )
                    )

        return tuple(result)

from collections.abc import Sequence
from dataclasses import asdict
from pathlib import Path
from typing import List, Optional

import aiofiles
import aiosqlite

from ...entity import Entity, Todo
from ..repository import Repository

QUERIES_DIRECTORY = Path(__file__).parent / "queries"


class SqliteRepository(Repository[Todo]):
    __db_path: str

    @classmethod
    def create(cls, db_path: str) -> "SqliteRepository":
        repository = cls()
        repository.__db_path = db_path
        return repository

    async def save(self, entity: Entity[Todo]) -> None:
        async with aiofiles.open(QUERIES_DIRECTORY / "save.sql", "r") as file:
            query = await file.read()

        async with aiosqlite.connect(self.__db_path) as db:
            parameters = asdict(entity.data)
            parameters["id"] = entity.id
            await db.execute(
                query,
                parameters=parameters,
            )
            await db.commit()

    async def remove(self, id: str) -> Optional[Entity[Todo]]:
        async with aiofiles.open(QUERIES_DIRECTORY / "remove.sql", "r") as file:
            query = await file.read()
        async with aiosqlite.connect(self.__db_path) as db:
            parameters = {"id": id}
            await db.execute(
                query,
                parameters,
            )
            await db.commit()

    async def get_by_id(self, id: str) -> Optional[Entity[Todo]]:
        async with aiofiles.open(QUERIES_DIRECTORY / "get_by_id.sql", "r") as file:
            query = await file.read()
        async with aiosqlite.connect(self.__db_path) as db:
            parameters = {"id": id}
            async with db.execute(
                query,
                parameters,
            ) as cursor:
                async for row in cursor:
                    return Entity.create(
                        Todo(*row[1:]),
                        id=row[0],
                    )

    async def get_all(self) -> Sequence[Entity[Todo]]:
        result: List[Entity[Todo]] = []
        async with aiofiles.open(QUERIES_DIRECTORY / "get_all.sql", "r") as file:
            query = await file.read()
        async with aiosqlite.connect(self.__db_path) as db:
            async with db.execute(
                query,
            ) as cursor:
                async for row in cursor:
                    result.append(
                        Entity.create(
                            Todo(*row[1:]),
                            id=row[0],
                        )
                    )

        return result

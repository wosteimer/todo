from collections.abc import Sequence
from typing import TypeAlias

from ..entity import Entity
from ..entity.todo import Todo
from ..repository import Repository

Response: TypeAlias = Sequence[Entity[Todo]]


class HomeUseCase:
    __todo_repository: Repository[Todo]

    @classmethod
    def create(cls, todo_repository: Repository[Todo]) -> "HomeUseCase":
        use_case = cls()
        use_case.__todo_repository = todo_repository
        return use_case

    async def perform(self) -> Response:
        return await self.__todo_repository.get_all()

from typing import Optional

from ..entity import Entity, Todo
from ..repository import Repository


class RemoveUseCase:
    __todo_repository: Repository[Todo]

    @classmethod
    def create(cls, todo_repository: Repository[Todo]):
        use_case = cls()
        use_case.__todo_repository = todo_repository
        return use_case

    async def perform(self, request: str) -> Optional[Entity[Todo]]:
        return await self.__todo_repository.remove(request)

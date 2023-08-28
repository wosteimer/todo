from datetime import datetime

from ..entity import Entity, Todo
from ..repository.repository import Repository


class AddUseCase:
    __todo_repository: Repository[Todo]

    @classmethod
    def create(cls, todo_repository: Repository[Todo]) -> "AddUseCase":
        use_case = cls()
        use_case.__todo_repository = todo_repository

        return use_case

    async def perform(self, request: str) -> Entity[Todo]:
        date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        entity = Entity.create(Todo(request, date, date))
        await self.__todo_repository.save(entity)

        return entity

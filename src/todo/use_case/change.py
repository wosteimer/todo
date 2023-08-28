from dataclasses import replace
from datetime import datetime
from typing import Optional

from ..entity import Entity
from ..entity.todo import Todo
from ..repository import Repository


class ChangeUsecase:
    __todo_repository: Repository[Todo]

    @classmethod
    def create(cls, todo_repository: Repository[Todo]) -> "ChangeUsecase":
        use_case = cls()
        use_case.__todo_repository = todo_repository

        return use_case

    async def perform(self, id: str) -> Optional[Entity[Todo]]:
        match await self.__todo_repository.get_by_id(id):
            case None:
                return

            case entity:
                updated_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                new_todo = replace(
                    entity.data,
                    its_done=not entity.data.its_done,
                    updated_at=updated_at,
                )
                new_entity = Entity.create(new_todo, id=id)
                await self.__todo_repository.save(new_entity)

                return new_entity

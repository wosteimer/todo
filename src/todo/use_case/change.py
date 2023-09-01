from typing import Optional

from ..entity import Entity
from ..entity.todo import Todo, set_its_done
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
                new_entity = Entity.create(
                    set_its_done(entity.data, not entity.data.its_done), id=entity.id
                )
                await self.__todo_repository.save(new_entity)

                return new_entity

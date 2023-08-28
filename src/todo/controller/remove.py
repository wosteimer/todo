from starlette.requests import Request
from starlette.responses import HTMLResponse, Response

from ..entity.todo import Todo
from ..repository.repository import Repository
from ..use_case.remove import RemoveUseCase
from .controller import Controller


class RemoveController(Controller[Request, Response]):
    __use_case: RemoveUseCase

    @classmethod
    def create(cls, repository: Repository[Todo]) -> "RemoveController":
        controller = cls()
        controller.__use_case = RemoveUseCase.create(repository)

        return controller

    async def perform(self, request: Request) -> Response:
        id = request.path_params["id"]
        await self.__use_case.perform(id)
        return HTMLResponse(status_code=200)

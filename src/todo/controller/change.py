from starlette.requests import Request
from starlette.responses import HTMLResponse, Response
from starlette.templating import Jinja2Templates

from ..entity.todo import Todo
from ..repository.repository import Repository
from ..use_case.change import ChangeUsecase
from .controller import Controller


class ChangeController(Controller[Request, Response]):
    __template: Jinja2Templates
    __use_case: ChangeUsecase

    @classmethod
    def create(
        cls, template: Jinja2Templates, repository: Repository[Todo]
    ) -> "ChangeController":
        controller = cls()
        controller.__template = template
        controller.__use_case = ChangeUsecase.create(repository)

        return controller

    async def perform(self, request: Request) -> Response:
        id = request.path_params["id"]
        match await self.__use_case.perform(id):
            case None:
                return HTMLResponse(status_code=400)
            case entity:
                return self.__template.TemplateResponse(
                    request,
                    "todo_item.html",
                    {"id": entity.id, "todo": entity.data},
                    status_code=200,
                )

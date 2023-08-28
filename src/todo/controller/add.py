from starlette.requests import Request
from starlette.responses import Response
from starlette.templating import Jinja2Templates

from ..entity.todo import Todo
from ..repository.repository import Repository
from ..use_case.add import AddUseCase
from .controller import Controller


class AddController(Controller[Request, Response]):
    __template: Jinja2Templates
    __use_case: AddUseCase

    @classmethod
    def create(
        cls, template: Jinja2Templates, repository: Repository[Todo]
    ) -> "AddController":
        controller = cls()
        controller.__template = template
        controller.__use_case = AddUseCase.create(repository)

        return controller

    async def perform(self, request: Request) -> Response:
        form = await request.form()
        match form.get("text"):
            case "":
                return Response(status_code=400)
            case str(value):
                text = value
            case _:
                return Response(status_code=400)

        entity = await self.__use_case.perform(text)
        return self.__template.TemplateResponse(
            request,
            "todo_item.html",
            {"id": entity.id, "todo": entity.data},
            status_code=201,
        )

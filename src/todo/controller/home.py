from starlette.requests import Request
from starlette.responses import Response
from starlette.templating import Jinja2Templates

from ..entity.todo import Todo
from ..repository.repository import Repository
from ..use_case.home import HomeUseCase
from .controller import Controller


class HomeController(Controller[Request, Response]):
    __template: Jinja2Templates
    __use_case: HomeUseCase

    @classmethod
    def create(
        cls, template: Jinja2Templates, repository: Repository[Todo]
    ) -> "HomeController":
        controller = cls()
        controller.__template = template
        controller.__use_case = HomeUseCase.create(repository)
        return controller

    async def perform(self, request: Request) -> Response:
        entitys = await self.__use_case.perform()
        todos = ((entity.id, entity.data) for entity in entitys)
        return self.__template.TemplateResponse(request, "home.html", {"todos": todos})

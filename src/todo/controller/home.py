from collections.abc import Sequence
from starlette.requests import Request
from starlette.responses import HTMLResponse, Response

from todo.template.home import Home
from todo.template.todo import TodoProps

from ..entity.todo import Todo
from ..repository.repository import Repository
from ..use_case.home import HomeUseCase
from .controller import Controller


class HomeController(Controller[Request, Response]):
    __use_case: HomeUseCase

    @classmethod
    def create(cls, repository: Repository[Todo]) -> "HomeController":
        controller = cls()
        controller.__use_case = HomeUseCase.create(repository)
        return controller

    async def perform(self, request: Request) -> Response:
        entitys = await self.__use_case.perform()
        todos: Sequence[TodoProps] = [
            {
                "id": entity.id,
                "url_for_bars": str(request.url_for("static", path="bars.svg")),
                "url_for_change": str(request.url_for("change", id=entity.id)),
                "url_for_remove": str(request.url_for("remove", id=entity.id)),
                "its_done": entity.data.its_done,
                "content": entity.data.text,
            }
            for entity in entitys
        ]
        html = Home(
            url_for_style=str(request.url_for("static", path="/css/style.css")),
            url_for_add=str(request.url_for("add")),
            url_for_spinner=str(request.url_for("static", path="/spinner.svg")),
            todos=todos,
        )
        return HTMLResponse("<!doctype html>\n" + html.build())

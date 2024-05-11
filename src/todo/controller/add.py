from starlette.requests import Request
from starlette.responses import HTMLResponse, Response

from ..entity.todo import Todo
from ..template.todo import Todo as HTMLTodo
from ..repository.repository import Repository
from ..use_case.add import AddUseCase
from .controller import Controller


class AddController(Controller[Request, Response]):
    __use_case: AddUseCase

    @classmethod
    def create(cls, repository: Repository[Todo]) -> "AddController":
        controller = cls()
        controller.__use_case = AddUseCase.create(repository)

        return controller

    async def perform(self, request: Request) -> Response:
        form = await request.form()
        match form.get("text"):
            case str(value) if value != "":
                text = value
            case _:
                return Response(status_code=400)

        entity = await self.__use_case.perform(text)
        html = HTMLTodo(
            id=entity.id,
            url_for_bars=str(request.url_for("static", path="bars.svg")),
            url_for_change=str(request.url_for("change", id=entity.id)),
            url_for_remove=str(request.url_for("remove", id=entity.id)),
            its_done=entity.data.its_done,
            content=entity.data.text,
        )
        return HTMLResponse("<!doctype html>\n" + html.build())

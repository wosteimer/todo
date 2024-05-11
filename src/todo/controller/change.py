from starlette.requests import Request
from starlette.responses import HTMLResponse, Response

from ..entity.todo import Todo
from ..repository.repository import Repository
from ..use_case.change import ChangeUsecase
from .controller import Controller
from ..template.todo import Todo as HTMLTodo


class ChangeController(Controller[Request, Response]):
    __use_case: ChangeUsecase

    @classmethod
    def create(cls, repository: Repository[Todo]) -> "ChangeController":
        controller = cls()
        controller.__use_case = ChangeUsecase.create(repository)

        return controller

    async def perform(self, request: Request) -> Response:
        id = request.path_params["id"]
        match await self.__use_case.perform(id):
            case None:
                return HTMLResponse(status_code=400)
            case entity:
                html = HTMLTodo(
                    id=entity.id,
                    url_for_bars=str(request.url_for("static", path="bars.svg")),
                    url_for_change=str(request.url_for("change", id=entity.id)),
                    url_for_remove=str(request.url_for("remove", id=entity.id)),
                    its_done=entity.data.its_done,
                    content=entity.data.text,
                )
                return HTMLResponse("<!doctype html>\n" + html.build())

from collections.abc import Sequence

from starlette.routing import BaseRoute, Mount, Route
from starlette.staticfiles import StaticFiles
from starlette.templating import Jinja2Templates

from .controller.add import AddController
from .controller.change import ChangeController
from .controller.home import HomeController
from .controller.remove import RemoveController
from .entity.todo import Todo
from .repository.repository import Repository


def create_routes(
    template: Jinja2Templates, repository: Repository[Todo], static_files_directory: str
) -> Sequence[BaseRoute]:
    home = HomeController.create(template, repository)
    add = AddController.create(template, repository)
    remove = RemoveController.create(repository)
    change = ChangeController.create(template, repository)

    routes = (
        Route("/", home.perform, methods=["GET"], name="home"),
        Route("/add", add.perform, methods=["POST"], name="add"),
        Route("/remove/{id:str}", remove.perform, methods=["DELETE"], name="remove"),
        Route("/change/{id:str}", change.perform, methods=["PUT"], name="change"),
        Mount("/", app=StaticFiles(directory=static_files_directory), name="static"),
    )

    return routes

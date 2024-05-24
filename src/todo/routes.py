from collections.abc import Sequence
from pathlib import Path

from builder.styler import Styler
from starlette.routing import BaseRoute, Mount, Route
from starlette.staticfiles import StaticFiles

from .controller.create_todo import create_todo
from .controller.delete_todo import delete_todo
from .controller.show_modal import show_modal
from .controller.show_todos import show_todos
from .controller.update_todo import update_todo


def create_routes(static_files_directory: Path | str) -> Sequence[BaseRoute]:
    Styler.set_globals(f'@import "{Path(__file__).parent}/template/scss/globals.scss";')
    stylesheet = Styler.build_stylesheet()
    with open(Path(static_files_directory) / "css/style.css", "w") as file:
        file.write(stylesheet)
    routes = (
        Route("/", show_todos, methods=["GET"], name="home"),
        Route("/todo", create_todo, methods=["POST"], name="create_todo"),
        Route("/todo/{id:str}", delete_todo, methods=["DELETE"], name="delete_todo"),
        Route("/todo/{id:str}", update_todo, methods=["PATCH"], name="update_todo"),
        Route("/modal/{id:str}", show_modal, methods=["POST"], name="show_modal"),
        Mount("/", app=StaticFiles(directory=static_files_directory), name="static"),
    )

    return routes

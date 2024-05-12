from collections.abc import Sequence

from starlette.routing import BaseRoute, Mount, Route
from starlette.staticfiles import StaticFiles

from todo.controller.update_todo_controller import UpdateTodoController
from todo.controller.delete_todo_controller import DeleteTodoController

from .controller.create_todo_controller import CreateTodoController
from .controller.show_todos_controller import ShowTodosController
from pathlib import Path


def create_routes(static_files_directory: Path | str) -> Sequence[BaseRoute]:
    show_todos = ShowTodosController()
    create_todo = CreateTodoController()
    delete_todo = DeleteTodoController()
    update_todo = UpdateTodoController()

    routes = (
        Route("/", show_todos.handle, methods=["GET"], name="home"),
        Route("/todo", create_todo.handle, methods=["POST"], name="create_todo"),
        Route(
            "/todo/{id:str}", delete_todo.handle, methods=["DELETE"], name="delete_todo"
        ),
        Route(
            "/todo/{id:str}", update_todo.handle, methods=["PATCH"], name="update_todo"
        ),
        Mount("/", app=StaticFiles(directory=static_files_directory), name="static"),
    )

    return routes

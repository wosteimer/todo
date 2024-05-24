from collections.abc import Sequence

from starlette.requests import Request
from starlette.responses import HTMLResponse, Response

from todo.repository.todo_repository import TodoRepository
from todo.template.components.todo import TodoProps
from todo.use_case.show_todos import ShowTodos

from ..template.pages.home import Home


async def show_todos(request: Request) -> Response:
    todos: TodoRepository = request.state.todos
    case = ShowTodos(todos)
    outputs = await case.perform()
    todos_props: Sequence[TodoProps] = [
        {
            "id": str(output["id"]),
            "url_for_update_todo": str(
                request.url_for("update_todo", id=str(output["id"]))
            ),
            "url_for_delete_todo": str(
                request.url_for("delete_todo", id=str(output["id"]))
            ),
            "url_for_show_modal": str(
                request.url_for("show_modal", id=str(output["id"]))
            ),
            "its_done": output["its_done"],
            "content": output["content"],
        }
        for output in outputs
    ]
    html = Home(
        url_for_create_todo=str(request.url_for("create_todo")),
        todos=todos_props,
    )
    return HTMLResponse("<!doctype html>\n" + html.build())

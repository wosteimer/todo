from uuid import UUID

from returns import Err, Ok
from starlette.requests import Request
from starlette.responses import HTMLResponse, Response

from ..entity.todo import InvalidContentError
from ..errors import TodoNotFoundError
from ..repository.todo_repository import TodoRepository
from ..template.components.todo import Todo
from ..use_case.update_todo import Input, UpdateTodo


async def update_todo(request: Request) -> Response:
    todos: TodoRepository = request.state.todos
    case = UpdateTodo(todos)
    form = await request.form()
    content, its_done = form.get("content"), form.get("its_done")
    content = str(content) if content else None
    input: Input = {
        "id": UUID(request.path_params["id"]),
    }
    if content:
        input["content"] = content
    if its_done:
        input["its_done"] = str(its_done) == "true"
    result = await case.perform(**input)
    # fmt:off
    match result:
        case Err(err):
            match err:
                case TodoNotFoundError(): return HTMLResponse(status_code=404)
                case InvalidContentError(): return HTMLResponse(status_code=400)
        case Ok(output):
            id, content, its_done = str(output["id"]), output["content"], output["its_done"]
            html = Todo(
                id=id,
                url_for_update_todo=str(request.url_for("update_todo", id=id)),
                url_for_delete_todo=str(request.url_for("delete_todo", id=id)),
                url_for_show_modal=str(request.url_for("show_modal", id=id)),
                its_done=its_done,
                content=content,
            )
            return HTMLResponse(html.build())
    # fmt:on

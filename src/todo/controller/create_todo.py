from returns import Err, Ok
from starlette.requests import Request
from starlette.responses import HTMLResponse, Response

from ..repository.todo_repository import TodoRepository
from ..template.components.todo import Todo as HTMLTodo
from ..use_case.create_todo import CreateTodo


async def create_todo(request: Request) -> Response:
    todos: TodoRepository = request.state.todos
    case = CreateTodo(todos)
    form = await request.form()
    content = str(form.get("content", ""))
    result = await case.perform(content=content)
    # fmt: off
    match result:
        case Err(): return HTMLResponse(status_code=400)
        case Ok(output):
            id, content, its_done = str(output["id"]), output["content"], output["its_done"]
            html = HTMLTodo(
                id=id,
                url_for_update_todo=str(request.url_for("update_todo", id=id)),
                url_for_delete_todo=str(request.url_for("delete_todo", id=id)),
                url_for_show_modal=str(request.url_for("show_modal", id=id)),
                its_done=its_done,
                content=content,
            )
            return HTMLResponse(html.build())
    # fmt: on

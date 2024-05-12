from uuid import UUID
from starlette.requests import Request
from starlette.responses import HTMLResponse, Response

from ..template.todo import Todo as HTMLTodo
from ..repository.todo_repository import TodoRepository
from ..use_case.update_todo import Input, UpdateTodo


class UpdateTodoController:
    async def handle(self, request: Request) -> Response:
        todos: TodoRepository = request.state.todos
        case = UpdateTodo(todos)
        form = await request.form()
        content, its_done = form.get("content"), form.get("its_done")
        input: Input = {
            "id": UUID(request.path_params["id"]),
        }
        if content:
            input["content"] = str(content)
        if its_done:
            input["its_done"] = str(its_done) == "true"
        todo, err = await case.perform(**input)
        if err != None:
            return HTMLResponse(status_code=400)
        id, content, its_done = str(todo["id"]), todo["content"], todo["its_done"]
        html = HTMLTodo(
            id=id,
            url_for_bars=str(request.url_for("static", path="bars.svg")),
            url_for_update_todo=str(request.url_for("update_todo", id=id)),
            url_for_delete_todo=str(request.url_for("delete_todo", id=id)),
            its_done=its_done,
            content=content,
        )
        return HTMLResponse(html.build())

from starlette.requests import Request
from starlette.responses import HTMLResponse, Response

from todo.repository.todo_repository import TodoRepository
from todo.use_case.create_todo import CreateTodo

from ..template.todo import Todo as HTMLTodo


class CreateTodoController:
    async def handle(self, request: Request) -> Response:
        todos: TodoRepository = request.state.todos
        case = CreateTodo(todos)
        form = await request.form()
        content = str(form.get("content", ""))
        if content == "" or len(content) > 24:
            return Response(status_code=400)
        todo = await case.perform(content=content)
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

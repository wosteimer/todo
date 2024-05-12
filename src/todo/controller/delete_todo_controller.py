from uuid import UUID
from starlette.requests import Request
from starlette.responses import HTMLResponse, Response

from todo.repository.todo_repository import TodoRepository
from todo.use_case.delete_todo import DeleteTodo


class DeleteTodoController:
    async def handle(self, request: Request) -> Response:
        todos: TodoRepository = request.state.todos
        case = DeleteTodo(todos)
        id = UUID(request.path_params["id"])
        _, err = await case.perform(id=id)
        if err != None:
            return HTMLResponse(status_code=400)
        return HTMLResponse(status_code=200)

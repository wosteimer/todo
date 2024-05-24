from uuid import UUID

from returns import Err, Ok
from starlette.requests import Request
from starlette.responses import HTMLResponse, Response

from todo.repository.todo_repository import TodoRepository
from todo.use_case.delete_todo import DeleteTodo


async def delete_todo(request: Request) -> Response:
    todos: TodoRepository = request.state.todos
    case = DeleteTodo(todos)
    id = UUID(request.path_params["id"])
    result = await case.perform(id=id)
    # fmt: off
    match result:
        case Ok(): return HTMLResponse(status_code=200)
        case Err():return HTMLResponse(status_code=404)
    # fmt: on

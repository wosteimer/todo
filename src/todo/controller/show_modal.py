from starlette.requests import Request
from starlette.responses import HTMLResponse, Response

from todo.template.components.modal import Modal


async def show_modal(request: Request) -> Response:
    form = await request.form()
    content = str(form.get("content", ""))
    id = request.path_params["id"]
    html = Modal(
        id=id,
        value=content,
        url_for_update_todo=str(request.url_for("update_todo", id=id)),
        its_open=True,
    )
    return HTMLResponse(html.build())

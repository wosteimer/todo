from ..text_input import TextInput
from .styles import Background, Container


def Modal(id: str, url_for_update_todo: str, value: str, its_open: bool = False):
    # fmt: off
    return Background(
        id="modal",
        classes=["show"] if its_open else [], 
        extra_props={
            "hx-on:click": (                         
                "htmx.removeClass(this, 'show');"
                "htmx.addClass(this, 'hide');"
            )
        }, 
        children=[
            Container(
                extra_props={
                    "hx-on:click": "event.stopPropagation()",
                    "hx-on::after-request": ( 
                        "htmx.removeClass(htmx.find('#modal'), 'show');"
                        "htmx.addClass(htmx.find('#modal'), 'hide');"
                    )
                },
                children=[TextInput(
                    method="patch",
                    submit_text="Ok",
                    target=f"#todo-{id}",
                    swap="outerHTML settle:0.25s",
                    url=url_for_update_todo,
                    value=value,
                )
        ])
        ])


# fmt: on

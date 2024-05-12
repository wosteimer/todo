from builder.tags import I, P, Button, Div, Img, Li
from typing import TypedDict, Unpack


class TodoProps(TypedDict):
    id: str
    url_for_bars: str
    url_for_update_todo: str
    url_for_delete_todo: str
    its_done: bool
    content: str


def Todo(**props: Unpack[TodoProps]):
    id, url_for_bars, url_for_update_todo, url_for_delete_todo, its_done, content = (
        props["id"],
        props["url_for_bars"],
        props["url_for_update_todo"],
        props["url_for_delete_todo"],
        props["its_done"],
        props["content"],
    )
    # fmt: off
    return Li(id=f"todo-{id}", children=[
        Div(id=f"indicator-{id}", classes=["htmx-indicator", "todo-loading"], children=[
            Img(src=url_for_bars, alt="carregando")
        ]),
        Div(classes=["todo-content"], children=[
            P(      
            hx_patch=url_for_update_todo,
            hx_target=f"#todo-{id}",
            hx_swap="outerHTML",
            hx_indicator=f"#indicator-{id}",
            hx_vals = f"js:{{its_done: !{str(its_done).lower()}}}",
            children=[
                I(classes=["fa-regular", "fa-solid", "fa-square-check"]) if its_done 
                else 
                I(classes=["fa-regular", "fa-square"]),
                content
            ]
            ),
            Button(      
            classes=["remove-button"],
            hx_delete=url_for_delete_todo,
            hx_target=f"#todo-{id}",
            hx_indicator=f"#indicator-{id}",
            hx_swap="delete",
            title="delete",
            children=[
                I(classes=["fa-solid", "fa-trash"])
            ]
            )
        ])
    ])


# fmt: on

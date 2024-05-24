from typing import TypedDict, Unpack

from builder.base import Text
from builder.tags import Del, Div, I, P

from .styles import (
    Checked,
    Container,
    FakeButton,
    FakeCheckBox,
    FakeContent,
    Left,
    NoChecked,
    Right,
    Skeleton,
)


class TodoProps(TypedDict):
    id: str
    its_done: bool
    url_for_delete_todo: str
    url_for_update_todo: str
    url_for_show_modal: str
    content: str


def Todo(**props: Unpack[TodoProps]):
    (
        id,
        its_done,
        url_for_delete_todo,
        url_for_update_todo,
        url_for_show_modal,
        content,
    ) = (
        props["id"],
        props["its_done"],
        props["url_for_delete_todo"],
        props["url_for_update_todo"],
        props["url_for_show_modal"],
        props["content"],
    )
    # fmt: off
    skeleton=Skeleton(children=[
        Div(children=[FakeCheckBox(), FakeContent()]),
        Div(children=[FakeButton()])
    ])
    return Container(classes=["todo"], id=f"todo-{id}", children=[
        Left(             
            extra_props={
                "hx-patch": url_for_update_todo,
                "hx-target": f"#todo-{id}",
                "hx-swap": "outerHTML settle:0.5s",
                "hx-indicator": f"#todo-{id} .{skeleton.classes[0]}",
                "hx-vals": f"js:{{its_done: {str(not its_done).lower()}}}",
            },
            children=[Checked(classes=["fa-regular", "fa-solid", "fa-square-check", "check-box"]), Del(children=[Text(content)])]
            if its_done else
            [NoChecked(classes=["fa-regular", "fa-square", "check-box"]), P(children=[Text(content)])]
        ),
        Right(
            extra_props={
                "hx-delete": url_for_delete_todo,
                "hx-target": f"#todo-{id}",
                "hx-indicator": f"#todo-{id} .{skeleton.classes[0]}",
                "hx-swap": "delete swap:0.5s",
            },
            title="delete",
            children=[I(classes=["fa-solid", "fa-trash"])],
        )
        if its_done else
        Right(
            extra_props={
                "hx-post": url_for_show_modal,
                "hx-target": "#modal",
                "hx-indicator": "#modal",
                "hx-swap": "outerHTML settle:0.25s",
                "hx-vals": f"js:{{content: '{content}'}}",
            },
            title="edit", 
            children=[I(classes=["fa-solid", "fa-pen"])]
        ),
        skeleton
    ])


# fmt: on

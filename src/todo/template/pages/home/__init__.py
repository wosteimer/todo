from collections.abc import Sequence
from typing import TypedDict, Unpack

from builder.base import Tag, Text
from builder.tags import A, I, Ul

from ...components.modal import Modal
from ...components.text_input import TextInput
from ...components.todo import Todo, TodoProps
from ..base import Base
from .styles import Container, Footer, Header, Main


class HomeProps(TypedDict):
    url_for_create_todo: str
    todos: Sequence[TodoProps]


def Home(**props: Unpack[HomeProps]) -> Tag:
    url_for_create_todo, todos = (
        props["url_for_create_todo"],
        props["todos"],
    )
    # fmt: off
    return Base(title="Todo App", root=
        Container(children=[
            Header(children=[TextInput(
                placeholder="Tem algo a Fazer?",
                submit_text="Adicionar",
                method="post",
                url=url_for_create_todo,
                target="#todo-list",
                swap="beforeend settle:0.5s",
            )]),
            Main(children=[Ul(id="todo-list", children=[
                Todo(**todo) for todo in todos
            ])]),
            Footer(children=[
                Text("feito com"), I(classes=["fa-solid", "fa-heart"]), Text("por"),
                A(href='https://wosteimer.github.io/my-links', target='_blank', children=[Text("@decadente")]),
            ]),
            Modal("", "", "")
        ])
    )
    # fmt: on

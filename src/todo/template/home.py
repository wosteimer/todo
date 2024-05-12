from collections.abc import Sequence
from typing import TypedDict, Unpack
from builder.base import Tag
from builder.tags import (
    A,
    I,
    Button,
    Div,
    Footer,
    Form,
    Header,
    Img,
    Input,
    Main,
    Span,
    Ul,
)
from todo.template.base import Base
from todo.template.todo import Todo, TodoProps


class HomeProps(TypedDict):
    url_for_style: str
    url_for_create_todo: str
    url_for_spinner: str
    todos: Sequence[TodoProps]


def Home(**props: Unpack[HomeProps]) -> Tag:
    url_for_style, url_for_create_todo, url_for_spinner, todos = (
        props["url_for_style"],
        props["url_for_create_todo"],
        props["url_for_spinner"],
        props["todos"],
    )
    # fmt: off
    return Base(title="Todo App", url_for_style=url_for_style, children=[
        Div(classes=["container"], children=[
            Header([Form(
                hx_post=url_for_create_todo, 
                hx_target="#todo-list", 
                hx_swap="beforeend",
                hx_indicator="#button",
                hx_ext="disable-element",
                hx_disable_element="#button",
                children=[
                    Input(
                        required=True,
                        type="text",
                        name="content", 
                        placeholder="Tem algo a fazer?",
                        autocomplete="off",
                        maxlength=24, 
                    ),
                    Button(classes=["submit-button"], id="button", type="submit", children=[
                        Img(
                            classes=["htmx-indicator", "indicator"],
                            src=url_for_spinner, 
                            alt="Carregando"
                        ),
                        Span(classes=["submit-button-content"], children=["Adicionar"])
                    ]),
                ]
            )]),
            Main([Ul(id="todo-list", children=[
                Todo(**todo) for todo in todos
            ])]),
            Footer([
                "feito com", I(classes=["fa-solid", "fa-heart"]), "por",
                A(href='https://wosteimer.github.io/my-links', target='_blank', children=["@decadente"]),
            ])
        ])
    ])
    # fmt: on

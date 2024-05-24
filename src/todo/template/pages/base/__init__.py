from typing import TypedDict, Unpack

from builder.base import Tag
from builder.tags import Body, Head, Html, Link, Meta, Script, Title

from .styles import Root


class BaseProps(TypedDict):
    title: str
    root: Tag


def Base(**props: Unpack[BaseProps]) -> Tag:
    title, root = (
        props["title"],
        props["root"],
    )
    # fmt: off
    return Html(lang="pt-BR", children=[
        Head(children=[
            Title(content=title),
            Meta(charset="UTF-8"),
            Meta(name="description", content="A simple todo application made with python and htmx"),
            Meta(name="viewport", content="width=device-width, initial-scale=1"),
            Meta(name="theme-color", media="(prefers-color-scheme: light)", content="#fafafa"),
            Meta(name="theme-color", media="(prefers-color-scheme: dark)", content="#242424"),
            Link(rel="stylesheet", href="/css/style.css"),
            Link(rel="preconnect", href="https://fonts.googleapis.com"),
            Link(rel="preconnect", href="https://fonts.gstatic.com", crossorigin=""),
            Link(rel="stylesheet", href="https://fonts.googleapis.com/css2?family=Roboto:wght@400;700&display=swap"),
            Script(
                src="https://unpkg.com/htmx.org@1.9.12",
                integrity="sha384-ujb1lZYygJmzgSwoxRggbCHcjc0rB2XoQrxeTUQyRjrOnlCoYta87iKBWq3EsdM2",
                crossorigin="anonymous",
            ),
            Script(src="https://kit.fontawesome.com/9c12109b80.js", crossorigin="anonymous") 
        ]),
        Body(children=[Root(children=[root])])
    ])
    # fmt: on

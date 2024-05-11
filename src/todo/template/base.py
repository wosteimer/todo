from collections.abc import Sequence
from typing import TypedDict, Unpack
from builder.base import Tag
from builder.tags import Body, Head, Html, Link, Meta, Script, Title


class BaseProps(TypedDict):
    title: str
    url_for_style: str
    children: Sequence[Tag]


def Base(**props: Unpack[BaseProps]) -> Tag:
    title, url_for_style, children = (
        props["title"],
        props["url_for_style"],
        props["children"],
    )
    # fmt: off
    return Html(lang="pt-BR", children=[
        Head([
            Title(title),
            Meta(charset="UTF-8"),
            Meta(name="description", content="A simple todo application made with python and htmx"),
            Meta(name="viewport", content="width=device-width, initial-scale=1"),
            Meta(name="theme-color", media="(prefers-color-scheme: light)", content="#fafafa"),
            Meta(name="theme-color", media="(prefers-color-scheme: dark)", content="#242424"),
            Link(rel="stylesheet", href=url_for_style),
            Link(rel="preconnect", href="https://fonts.googleapis.com"),
            Link(rel="preconnect", href="https://fonts.gstatic.com", crossorigin=""),
            Link(rel="stylesheet", href="https://fonts.googleapis.com/css2?family=Roboto:wght@400;700&display=swap"),
            Script(
                src="https://unpkg.com/htmx.org@1.9.12",
                integrity="sha384-ujb1lZYygJmzgSwoxRggbCHcjc0rB2XoQrxeTUQyRjrOnlCoYta87iKBWq3EsdM2",
                crossorigin="anonymous",
            ),
            Script(src="https://unpkg.com/htmx.org/dist/ext/disable-element.js"),
            Script(src="https://kit.fontawesome.com/9c12109b80.js", crossorigin="anonymous") 
        ]),
        Body(children)
    ])
    # fmt: on

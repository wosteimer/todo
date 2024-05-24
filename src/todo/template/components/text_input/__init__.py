from collections.abc import Mapping
from typing import Literal, NotRequired, TypedDict, Unpack
from uuid import uuid4

from builder.base import Prop, Text

from ..spinner import Spinner
from .styles import Container, Submit, SubmitText, TextField


class Props(TypedDict):
    placeholder: NotRequired[str]
    value: NotRequired[str]
    submit_text: str
    method: Literal["post", "put", "patch", "delete"]
    url: str
    target: str
    swap: str


# fmt: off
def TextInput(**props: Unpack[Props]):
    placeholder, value, submit_text, method, url, target, swap = (
        props.get("placeholder",""),
        props.get("value", ""),
        props["submit_text"],
        props["method"],
        props["url"],
        props["target"],
        props["swap"],
    )
    submit_id = f"submit-{str(uuid4()).split("-")[0]}"
    return Container(
        extra_props={
            f"hx-{method}": url, 
            "hx-target": target, 
            "hx-swap": swap,
            "hx-indicator": f"#{submit_id}",
            "hx-disable-elt": f"#{submit_id}",
        }, 
        children=[
            TextField(
                placeholder=placeholder,
                value=value,
                required=True,
                type="text",
                name="content", 
                autocomplete="off",
                autofocus=True,
                maxlength=24,
                extra_props={
                    "hx-on:focus": "this.select()"
                }
            ), 
            Submit(id=submit_id, type="submit", children=[
                Spinner(), 
                SubmitText(children=[Text(submit_text)])
            ])
        ]
    )
# fmt: on

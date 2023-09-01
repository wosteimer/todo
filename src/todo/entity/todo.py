from dataclasses import dataclass, replace
from datetime import datetime


@dataclass(slots=True, frozen=True)
class Todo:
    text: str
    created_at: str
    updated_at: str
    its_done: bool = False


def set_its_done(todo: Todo, its_done: bool) -> "Todo":
    return replace(
        todo,
        its_done=its_done,
        updated_at=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    )

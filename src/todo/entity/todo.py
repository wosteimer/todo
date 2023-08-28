from dataclasses import dataclass


@dataclass(slots=True, frozen=True)
class Todo:
    text: str
    created_at: str
    updated_at: str
    its_done: bool = False

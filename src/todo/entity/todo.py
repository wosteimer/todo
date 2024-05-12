from __future__ import annotations
from dataclasses import dataclass, replace
from datetime import datetime, timezone
from typing import TypedDict, Unpack
from uuid import UUID, uuid4


class UpdateProps(TypedDict, total=False):
    content: str
    its_done: bool


@dataclass(slots=True, frozen=True)
class Todo:
    id: UUID
    content: str
    its_done: bool
    created_at: datetime
    updated_at: datetime

    @classmethod
    def create(cls, content: str) -> Todo:
        id = uuid4()
        now = datetime.now(timezone.utc)
        return cls(id, content, False, now, now)

    def update(self, **props: Unpack[UpdateProps]) -> Todo:
        return replace(self, **props, updated_at=datetime.now(timezone.utc))

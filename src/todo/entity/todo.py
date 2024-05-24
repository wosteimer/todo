from __future__ import annotations

from copy import copy
from datetime import datetime, timezone
from typing import Optional
from uuid import UUID, uuid4

from returns import Err, Ok, Result

from ..errors import InvalidContentError


class Content(str):
    @classmethod
    def create(cls, content: str) -> Result[Content, InvalidContentError]:
        if len(content) > 24 or content == "":
            return Err(InvalidContentError())
        return Ok(cls(content))


class Todo:
    __id: UUID
    __content: Content
    __its_done: bool
    __created_at: datetime
    __updated_at: datetime

    @property
    def id(self) -> UUID:
        return self.__id

    @property
    def content(self) -> Content:
        return self.__content

    @property
    def its_done(self) -> bool:
        return self.__its_done

    @property
    def created_at(self) -> datetime:
        return self.__created_at

    @property
    def updated_at(self) -> datetime:
        return self.__updated_at

    @classmethod
    def create(cls, content: str) -> Result[Todo, InvalidContentError]:
        result = Content.create(content)
        # fmt:off
        match result:
            case Err(err): return Err(err)
            case Ok(content):
                id = uuid4()
                now = datetime.now(timezone.utc)
                todo = cls()
                todo.__id = id
                todo.__content = content
                todo.__its_done = False
                todo.__created_at = now
                todo.__updated_at = now
                return Ok(todo)
        # fmt:on

    @classmethod
    def restore(
        cls,
        id: UUID,
        content: str,
        its_done: bool,
        created_at: datetime,
        updated_at: datetime,
    ) -> Todo:
        todo = cls()
        todo.__id = id
        todo.__content = Content.create(content).unwrap()
        todo.__its_done = its_done
        todo.__created_at = created_at
        todo.__updated_at = updated_at
        return todo

    def update(
        self, content: Optional[str] = None, its_done: Optional[bool] = None
    ) -> Result[Todo, InvalidContentError]:
        # fmt:off
        todo = copy(self) 
        if content != None:
            result = Content.create(content)
            match result:
                case Err(err): return Err(err)
                case Ok(content): todo.__content = content 
        if its_done != None:
            todo.__its_done = its_done
        todo.__updated_at=datetime.now(timezone.utc)
        return Ok(todo)
        # fmt:on

import datetime

from pydantic import BaseModel


class NoteCreate(BaseModel):
    title: str
    content: str
    owner_id: int


class NoteUpdate(BaseModel):
    title: str | None = None
    content: str | None = None


class NoteRead(BaseModel):
    id: int
    title: str
    content: str
    owner_id: int
    created_at: datetime.datetime
    updated_at: datetime.datetime

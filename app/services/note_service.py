from typing import Annotated

from fastapi import Depends

from app.models import Note
from app.repos import NoteRepository
from app.schemas.note_schema import NoteCreate, NoteUpdate


class NoteService:
    def __init__(self, note_repo: Annotated[NoteRepository, Depends()]):
        self.note_repo = note_repo

    async def get_note(self, note_id: int) -> Note | None:
        note = await self.note_repo.get_note(note_id)
        if note:
            return note
        return None

    async def get_notes_by_user_id(self, user_id: int) -> list[Note]:
        notes = await self.note_repo.get_notes_by_user_id(user_id)
        return notes

    async def create_note(self, note_data: NoteCreate) -> Note:
        note = Note(**note_data.model_dump())
        note = await self.note_repo.create_note(note)
        return note

    async def update_note(self, note_id: int, note_data: NoteUpdate) -> Note | None:
        note = await self.note_repo.get_note(note_id)
        if not note:
            return None
        for key, value in note_data.model_dump(exclude_unset=True).items():
            setattr(note, key, value)
        return await self.note_repo.update_note(note)

    async def delete_note(self, note_id: int) -> bool:
        note = await self.note_repo.get_note(note_id)
        if not note:
            return False
        await self.note_repo.delete_note(note)
        return True

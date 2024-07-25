from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.db import get_session
from app.models import Note
from app.repos import NoteRepository
from app.schemas.note_schema import NoteCreate, NoteUpdate


class NoteService:
    def __init__(self, session: AsyncSession = Depends(get_session)):
        self.repo = NoteRepository(session)

    async def get_note(self, note_id: int) -> Note | None:
        note = await self.repo.get_note(note_id)
        if note:
            return note
        return None

    async def get_notes_by_user_id(self, user_id: int) -> list[Note]:
        notes = await self.repo.get_notes_by_user_id(user_id)
        return notes

    async def create_note(self, note_data: NoteCreate) -> Note:
        note = Note(**note_data.model_dump())
        note = await self.repo.create_note(note)
        return note

    async def update_note(self, note_id: int, note_data: NoteUpdate) -> Note | None:
        note = await self.repo.get_note(note_id)
        if not note:
            return None
        for key, value in note_data.model_dump(exclude_unset=True).items():
            setattr(note, key, value)
        return await self.repo.update_note(note)

    async def delete_note(self, note_id: int) -> bool:
        note = await self.repo.get_note(note_id)
        if not note:
            return False
        await self.repo.delete_note(note)
        return True

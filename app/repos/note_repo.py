from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.database.db import get_session
from app.models.note_model import Note


class NoteRepository:
    def __init__(self, session: Annotated[AsyncSession, Depends(get_session)]):
        self.session = session

    async def get_note(self, note_id: int) -> Note | None:
        return await self.session.get(Note, note_id)

    async def get_notes_by_user_id(self, user_id: int) -> list[Note]:
        result = await self.session.execute(
            select(Note).where(Note.owner_id == user_id)
        )
        return list(result.scalars().all())

    async def create_note(self, note: Note) -> Note:
        self.session.add(note)
        await self.session.commit()
        await self.session.refresh(note)
        return note

    async def update_note(self, note: Note) -> Note:
        await self.session.commit()
        await self.session.refresh(note)
        return note

    async def delete_note(self, note: Note) -> None:
        await self.session.delete(note)
        await self.session.commit()

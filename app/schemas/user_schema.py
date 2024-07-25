import datetime
import enum
from typing import TYPE_CHECKING

from pydantic import BaseModel, EmailStr

if TYPE_CHECKING:
    from app.schemas.note_schema import NoteRead


class UserRole(enum.Enum):
    ADMIN = "admin"
    USER = "user"


class UserCreate(BaseModel):
    email: EmailStr
    username: str
    password: str
    role: UserRole = UserRole.USER
    is_active: bool = False


class UserUpdate(BaseModel):
    email: EmailStr | None = None
    username: str | None = None
    password: str | None = None


class UserRead(BaseModel):
    id: int
    email: EmailStr
    username: str
    role: str
    is_active: bool
    notes: list["NoteRead"] | None = None
    created_at: datetime.datetime
    updated_at: datetime.datetime

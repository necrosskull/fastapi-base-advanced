import datetime
from typing import TYPE_CHECKING

from sqlalchemy import text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base

if TYPE_CHECKING:
    from app.models.note_model import Note


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    email: Mapped[str] = mapped_column(unique=True, index=True, nullable=False)
    username: Mapped[str] = mapped_column(unique=True, index=True, nullable=False)
    hashed_password: Mapped[str]
    role: Mapped[str] = mapped_column(nullable=False, default="user")
    is_active: Mapped[bool] = mapped_column(nullable=False, default=False)

    notes: Mapped[list["Note"]] = relationship(
        "Note", back_populates="owner", lazy="select"
    )

    created_at: Mapped[datetime.datetime] = mapped_column(
        server_default=text("TIMEZONE('utc', now())")
    )
    updated_at: Mapped[datetime.datetime] = mapped_column(
        server_default=text("TIMEZONE('utc', now())"),
        onupdate=text("TIMEZONE('utc', now())"),
    )

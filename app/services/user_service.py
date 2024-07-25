from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.db import get_session
from app.models.user_model import User
from app.repos import UserRepository
from app.schemas.user_schema import UserCreate, UserUpdate


class UserService:
    def __init__(self, session: AsyncSession = Depends(get_session)):
        self.repo = UserRepository(session)

    async def get_user(self, user_id: int) -> User | None:
        user = await self.repo.get_user(User(id=user_id))
        if user:
            return user
        return None

    async def get_user_by_email(self, email: str) -> User | None:
        user = await self.repo.get_user_by_email(email)
        if user:
            return user
        return None

    async def get_user_by_username(self, username: str) -> User | None:
        user = await self.repo.get_user_by_username(username)
        if user:
            return user
        return None

    async def create_user(self, user_data: UserCreate) -> User:
        user = User(
            email=user_data.email,
            username=user_data.username,
            hashed_password=user_data.password,
            role=str(user_data.role),
            is_active=user_data.is_active,
        )
        user = await self.repo.create_user(user)
        return user

    async def update_user(self, user_id: int, user_data: UserUpdate) -> User | None:
        user = await self.repo.get_user(User(id=user_id))
        if not user:
            return None
        for key, value in user_data.model_dump(exclude_unset=True).items():
            if key == "password":
                key = "hashed_password"
            setattr(user, key, value)
        user = await self.repo.update_user(user)
        return user

    async def delete_user(self, user_id: int) -> bool:
        user = await self.repo.get_user(User(id=user_id))
        if not user:
            return False
        await self.repo.delete_user(user)
        return True

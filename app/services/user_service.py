from typing import Annotated

from fastapi import Depends

from app.errors import UniqueException
from app.models.user_model import User
from app.repos import UserRepository
from app.schemas.user_schema import UserCreate, UserUpdate


class UserService:
    def __init__(self, user_repo: Annotated[UserRepository, Depends()]):
        self.user_repo = user_repo

    async def get_user(self, user_id: int) -> User | None:
        user = await self.user_repo.get_user(User(id=user_id))
        if user:
            return user
        return None

    async def get_user_by_email(self, email: str) -> User | None:
        user = await self.user_repo.get_user_by_email(email)
        if user:
            return user
        return None

    async def get_user_by_username(self, username: str) -> User | None:
        user = await self.user_repo.get_user_by_username(username)
        if user:
            return user
        return None

    async def create_user(self, user_data: UserCreate) -> User:
        user = User(
            email=user_data.email,
            username=user_data.username,
            hashed_password=user_data.password,
            role=user_data.role.value,
            is_active=user_data.is_active,
        )
        try:
            user = await self.user_repo.create_user(user)
        except UniqueException as e:
            raise UniqueException(e, extra_info=e.extra_info) from e
        return user

    async def update_user(self, user_id: int, user_data: UserUpdate) -> User | None:
        user = await self.user_repo.get_user(User(id=user_id))
        if not user:
            return None
        for key, value in user_data.model_dump(exclude_unset=True).items():
            if key == "password":
                key = "hashed_password"
            setattr(user, key, value)
        user = await self.user_repo.update_user(user)
        return user

    async def delete_user(self, user_id: int) -> bool:
        user = await self.user_repo.get_user(User(id=user_id))
        if not user:
            return False
        await self.user_repo.delete_user(user)
        return True

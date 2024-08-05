import uuid
from typing import Annotated

from fastapi import Depends
from passlib.context import CryptContext

from app.database.redis import redis_client
from app.errors.errors import UniqueException
from app.models.user_model import User
from app.schemas.user_schema import UserCreate, UserRole
from app.services.user_service import UserService

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class AuthService:
    def __init__(self, user_service: Annotated[UserService, Depends()]):
        self.user_service = user_service

    @staticmethod
    def verify_password(plain_password, hashed_password):
        return pwd_context.verify(plain_password, hashed_password)

    async def register(self, user_data: UserCreate) -> User:
        hashed_password = pwd_context.hash(user_data.password)
        user_data.password = hashed_password
        user_data.role = UserRole.USER
        user_data.is_active = False
        try:
            user = await self.user_service.create_user(user_data)
        except UniqueException as e:
            raise UniqueException(e, e.extra_info) from e
        return user

    async def login(self, username: str, password: str) -> str:
        user = await self.user_service.get_user_by_username(username)
        if not user:
            raise ValueError("Invalid username or password")

        if not self.verify_password(pwd_context.hash(password), user.hashed_password):
            raise ValueError("Invalid username or password")

        session_id = str(uuid.uuid4())
        await redis_client.set(session_id, user.id, ex=3600)  # Сессия действует 1 час
        return session_id

    async def get_user_by_session(self, session_id: str) -> User | None:
        user_id = await redis_client.get(session_id)
        if not user_id:
            return None
        user = await self.user_service.get_user(int(user_id))
        return user

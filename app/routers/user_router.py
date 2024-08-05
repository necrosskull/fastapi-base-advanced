from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException

from app.errors import UniqueException
from app.schemas.user_schema import UserCreate, UserRead
from app.services.auth import AuthService

router = APIRouter(prefix="/v1/users", tags=["users"])


@router.post("/register", response_model=UserRead)
async def register(user_data: UserCreate, service: Annotated[AuthService, Depends()]):
    try:
        user = await service.register(user_data)
    except UniqueException as e:
        raise HTTPException(status_code=400, detail=f"{e}, {e.extra_info}")
    return user

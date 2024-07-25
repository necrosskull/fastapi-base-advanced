from fastapi import APIRouter

router = APIRouter(prefix="/v1/auth", tags=["auth"])


@router.get("/login")
async def login():
    return {"message": "Login route"}

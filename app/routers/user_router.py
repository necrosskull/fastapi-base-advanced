from fastapi import APIRouter

router = APIRouter(prefix="/v1/users", tags=["users"])


@router.get("/user")
async def create_user():
    return {"message": "Create user route"}

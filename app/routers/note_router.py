from fastapi import APIRouter

router = APIRouter(prefix="/v1/notes", tags=["notes"])


@router.get("/note")
async def create_note():
    return {"message": "Create note route"}

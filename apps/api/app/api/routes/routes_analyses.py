from fastapi import APIRouter

from app.core.auth import CurrentUser

router = APIRouter()


@router.get("")
def list_analyses(current_user: CurrentUser) -> dict[str, object]:
    return {
        "items": [],
        "message": "Analyses endpoint scaffolded for the authenticated workspace.",
    }

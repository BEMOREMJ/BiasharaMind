from fastapi import APIRouter

from app.core.auth import CurrentUser

router = APIRouter()


@router.get("")
def list_businesses(current_user: CurrentUser) -> dict[str, object]:
    return {
        "items": [],
        "message": "Businesses endpoint scaffolded for the authenticated workspace.",
    }

from fastapi import APIRouter

from app.core.auth import CurrentUser

router = APIRouter()


@router.get("")
def list_reports(current_user: CurrentUser) -> dict[str, object]:
    return {
        "items": [],
        "message": "Reports endpoint scaffolded for the authenticated workspace.",
    }

from fastapi import APIRouter


router = APIRouter()


@router.get("")
def list_reports() -> dict[str, object]:
    return {
        "items": [],
        "message": "Reports endpoint scaffolded. Listing logic will be added later.",
    }

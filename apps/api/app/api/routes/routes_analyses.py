from fastapi import APIRouter


router = APIRouter()


@router.get("")
def list_analyses() -> dict[str, object]:
    return {
        "items": [],
        "message": "Analyses endpoint scaffolded. Listing logic will be added later.",
    }

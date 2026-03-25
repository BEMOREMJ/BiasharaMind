from fastapi import APIRouter


router = APIRouter()


@router.get("")
def list_businesses() -> dict[str, object]:
    return {
        "items": [],
        "message": "Businesses endpoint scaffolded. Listing logic will be added later.",
    }

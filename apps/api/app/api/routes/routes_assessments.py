from fastapi import APIRouter


router = APIRouter()


@router.get("")
def list_assessments() -> dict[str, object]:
    return {
        "items": [],
        "message": "Assessments endpoint scaffolded. Listing logic will be added later.",
    }

from fastapi import APIRouter, HTTPException, status

from app.core.auth import CurrentUser
from app.schemas.assessment import (
    AssessmentCreate,
    AssessmentRead,
    AssessmentSubmit,
    AssessmentUpdate,
)
from app.services.assessment_service import assessment_service


router = APIRouter()


@router.get("/assessment", response_model=AssessmentRead)
def get_assessment(current_user: CurrentUser) -> AssessmentRead:
    assessment = assessment_service.get_assessment(current_user.id)
    if assessment is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Assessment not found",
        )
    return assessment


@router.post("/assessment", response_model=AssessmentRead, status_code=status.HTTP_201_CREATED)
def create_assessment(payload: AssessmentCreate, current_user: CurrentUser) -> AssessmentRead:
    existing = assessment_service.get_assessment(current_user.id)
    if existing is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Assessment already exists",
        )
    return assessment_service.create_assessment(payload, current_user.id)


@router.patch("/assessment", response_model=AssessmentRead)
def update_assessment(payload: AssessmentUpdate, current_user: CurrentUser) -> AssessmentRead:
    assessment = assessment_service.update_assessment(payload, current_user.id)
    if assessment is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Assessment not found",
        )
    return assessment


@router.post("/assessment/submit", response_model=AssessmentRead)
def submit_assessment(payload: AssessmentSubmit, current_user: CurrentUser) -> AssessmentRead:
    assessment = assessment_service.submit_assessment(payload, current_user.id)
    if assessment is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Assessment not found",
        )
    return assessment

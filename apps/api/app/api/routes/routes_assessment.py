from fastapi import APIRouter, HTTPException, status

from app.schemas.assessment import (
    AssessmentCreate,
    AssessmentRead,
    AssessmentSubmit,
    AssessmentUpdate,
)
from app.services.assessment_service import assessment_service


router = APIRouter()


@router.get("/assessment", response_model=AssessmentRead)
def get_assessment() -> AssessmentRead:
    assessment = assessment_service.get_assessment()
    if assessment is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Assessment not found",
        )
    return assessment


@router.post("/assessment", response_model=AssessmentRead, status_code=status.HTTP_201_CREATED)
def create_assessment(payload: AssessmentCreate) -> AssessmentRead:
    existing = assessment_service.get_assessment()
    if existing is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Assessment already exists",
        )
    return assessment_service.create_assessment(payload)


@router.patch("/assessment", response_model=AssessmentRead)
def update_assessment(payload: AssessmentUpdate) -> AssessmentRead:
    assessment = assessment_service.update_assessment(payload)
    if assessment is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Assessment not found",
        )
    return assessment


@router.post("/assessment/submit", response_model=AssessmentRead)
def submit_assessment(payload: AssessmentSubmit) -> AssessmentRead:
    assessment = assessment_service.submit_assessment(payload)
    if assessment is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Assessment not found",
        )
    return assessment

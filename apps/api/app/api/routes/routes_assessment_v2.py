from fastapi import APIRouter, HTTPException, status

from app.core.auth import CurrentUser
from app.v2.schemas.assessment import (
    AssessmentDefinitionRead,
    AssessmentRead,
    AssessmentSaveResponse,
    AssessmentWritePayload,
)
from app.v2.services.assessment import MissingBusinessProfileError, get_assessment_v2_service


router = APIRouter(prefix="/v2")


@router.get("/assessment/definition", response_model=AssessmentDefinitionRead)
def get_assessment_definition_v2(current_user: CurrentUser) -> AssessmentDefinitionRead:
    try:
        return get_assessment_v2_service().build_definition(current_user.id)
    except MissingBusinessProfileError as exc:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(exc)) from exc


@router.get("/assessment", response_model=AssessmentRead)
def get_assessment_v2(current_user: CurrentUser) -> AssessmentRead:
    assessment = get_assessment_v2_service().get_assessment(current_user.id)
    if assessment is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="V2 assessment not found")
    return assessment


@router.put("/assessment", response_model=AssessmentSaveResponse)
def save_assessment_v2(
    payload: AssessmentWritePayload,
    current_user: CurrentUser,
) -> AssessmentSaveResponse:
    try:
        return get_assessment_v2_service().save_assessment(payload, current_user.id)
    except MissingBusinessProfileError as exc:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(exc)) from exc
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(exc)) from exc


@router.post("/assessment/submit", response_model=AssessmentSaveResponse)
def submit_assessment_v2(
    payload: AssessmentWritePayload,
    current_user: CurrentUser,
) -> AssessmentSaveResponse:
    try:
        return get_assessment_v2_service().submit_assessment(payload, current_user.id)
    except MissingBusinessProfileError as exc:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(exc)) from exc
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(exc)) from exc

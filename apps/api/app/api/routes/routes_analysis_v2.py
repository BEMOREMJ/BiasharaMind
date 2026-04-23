from fastapi import APIRouter, HTTPException, status

from app.core.auth import CurrentUser
from app.v2.schemas.scoring import AnalysisRunRead
from app.v2.services.analysis import MissingSubmittedAssessmentError, get_analysis_v2_service


router = APIRouter(prefix="/v2")


@router.get("/analysis", response_model=AnalysisRunRead)
def get_analysis_v2(current_user: CurrentUser) -> AnalysisRunRead:
    analysis = get_analysis_v2_service().get_latest(current_user.id)
    if analysis is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="V2 analysis not found")
    return analysis


@router.post("/analysis/run", response_model=AnalysisRunRead)
def run_analysis_v2(current_user: CurrentUser) -> AnalysisRunRead:
    try:
        return get_analysis_v2_service().run_analysis(current_user.id)
    except MissingSubmittedAssessmentError as exc:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(exc)) from exc

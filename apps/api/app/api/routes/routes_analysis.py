from fastapi import APIRouter, HTTPException, status

from app.core.auth import CurrentUser
from app.schemas.analysis import AnalysisSummaryRead
from app.services.analysis_service import analysis_service


router = APIRouter()


@router.get("/analysis", response_model=AnalysisSummaryRead)
def get_analysis(current_user: CurrentUser) -> AnalysisSummaryRead:
    analysis = analysis_service.get_analysis(current_user.id)
    if analysis is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Analysis summary not found",
        )
    return analysis


@router.post("/analysis/run", response_model=AnalysisSummaryRead)
def run_analysis(current_user: CurrentUser) -> AnalysisSummaryRead:
    analysis = analysis_service.run_analysis(current_user.id)
    if analysis is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Assessment not found",
        )
    return analysis

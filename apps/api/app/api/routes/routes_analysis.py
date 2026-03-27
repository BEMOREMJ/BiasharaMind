from fastapi import APIRouter, HTTPException, status

from app.schemas.analysis import AnalysisSummaryRead
from app.services.analysis_service import analysis_service


router = APIRouter()


@router.get("/analysis", response_model=AnalysisSummaryRead)
def get_analysis() -> AnalysisSummaryRead:
    analysis = analysis_service.get_analysis()
    if analysis is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Analysis summary not found",
        )
    return analysis


@router.post("/analysis/run", response_model=AnalysisSummaryRead)
def run_analysis() -> AnalysisSummaryRead:
    analysis = analysis_service.run_analysis()
    if analysis is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Assessment not found",
        )
    return analysis

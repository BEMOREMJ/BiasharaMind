from fastapi import APIRouter, HTTPException, status

from app.core.auth import CurrentUser
from app.schemas.report import ReportRead
from app.services.report_service import report_service


router = APIRouter()


@router.get("/report", response_model=ReportRead)
def get_report(current_user: CurrentUser) -> ReportRead:
    report = report_service.get_report(current_user.id)
    if report is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Report not found",
        )
    return report


@router.post("/report/generate", response_model=ReportRead)
def generate_report(current_user: CurrentUser) -> ReportRead:
    report = report_service.generate_report(current_user.id)
    if report is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Required source data not found",
        )
    return report

from datetime import UTC, datetime
from uuid import uuid4

from app.repositories.report_repository import report_repository
from app.schemas.report import ReportBusinessSummary, ReportRead, ReportRoadmapPhase
from app.services.analysis_service import analysis_service
from app.services.business_profile_service import business_profile_service
from app.services.roadmap_service import roadmap_service


class ReportService:
    """Deterministic V1 report assembly from saved feature outputs."""

    def get_report(self, user_id: str) -> ReportRead | None:
        return report_repository.get(user_id)

    def generate_report(self, user_id: str) -> ReportRead | None:
        business_profile = business_profile_service.get_profile(user_id)
        analysis = analysis_service.get_analysis(user_id)
        roadmap = roadmap_service.get_roadmap(user_id)

        if business_profile is None or analysis is None or roadmap is None:
            return None

        report = ReportRead(
            id=f"report_{uuid4().hex}",
            analysis_id=analysis.id,
            format="json",
            storage_path=f"reports/{analysis.id}_report.json",
            created_at=datetime.now(UTC).isoformat(),
            business_summary=ReportBusinessSummary(
                business_name=business_profile.business_name,
                industry=business_profile.industry,
                country=business_profile.country,
                size_band=business_profile.size_band,
                team_size=business_profile.team_size,
                main_goal=business_profile.main_goal,
            ),
            overall_score=analysis.overall_score,
            category_scores=analysis.category_scores,
            strengths=analysis.top_strengths,
            risks=analysis.top_risks,
            priorities=analysis.top_priorities,
            roadmap_phases=[
                ReportRoadmapPhase(label="Days 0-30", actions=roadmap.days0to30),
                ReportRoadmapPhase(label="Days 31-60", actions=roadmap.days31to60),
                ReportRoadmapPhase(label="Days 61-90", actions=roadmap.days61to90),
            ],
            export_file_name=f"biasharamind-report-{analysis.id}.json",
        )

        return report_repository.save(report, user_id)


report_service = ReportService()

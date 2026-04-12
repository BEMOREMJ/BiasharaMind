from sqlalchemy import select, update

from app.db.session import session_scope
from app.models.report import ReportRecord
from app.schemas.analysis import AnalysisCategoryScore, PriorityRecommendation
from app.schemas.report import ReportBusinessSummary, ReportRead, ReportRoadmapPhase


def _to_schema(record: ReportRecord) -> ReportRead:
    return ReportRead(
        id=record.id,
        analysis_id=record.analysis_id,
        format=record.format,
        storage_path=record.storage_path,
        created_at=record.created_at.isoformat(),
        business_summary=ReportBusinessSummary.model_validate(record.business_summary),
        overall_score=float(record.overall_score),
        category_scores=[
            AnalysisCategoryScore.model_validate(item) for item in record.category_scores or []
        ],
        strengths=list(record.strengths or []),
        risks=list(record.risks or []),
        priorities=[
            PriorityRecommendation.model_validate(item) for item in record.priorities or []
        ],
        roadmap_phases=[ReportRoadmapPhase.model_validate(item) for item in record.roadmap_phases or []],
        export_file_name=record.export_file_name,
    )


class ReportRepository:
    """PostgreSQL-backed repository for generated reports."""

    def get(self) -> ReportRead | None:
        with session_scope() as session:
            record = session.scalar(
                select(ReportRecord)
                .where(ReportRecord.is_active.is_(True))
                .order_by(ReportRecord.created_at.desc())
                .limit(1)
            )
            if record is None:
                return None
            return _to_schema(record)

    def save(self, report: ReportRead) -> ReportRead:
        with session_scope() as session:
            session.execute(
                update(ReportRecord)
                .where(ReportRecord.is_active.is_(True))
                .values(is_active=False)
            )
            record = ReportRecord(
                id=report.id,
                user_id=None,
                analysis_id=report.analysis_id,
                format=report.format,
                storage_path=report.storage_path,
                business_summary=report.business_summary.model_dump(mode="json"),
                overall_score=report.overall_score,
                category_scores=[item.model_dump(mode="json") for item in report.category_scores],
                strengths=report.strengths,
                risks=report.risks,
                priorities=[item.model_dump(mode="json") for item in report.priorities],
                roadmap_phases=[item.model_dump(mode="json") for item in report.roadmap_phases],
                export_file_name=report.export_file_name,
            )
            session.add(record)
            session.flush()
            session.refresh(record)
            return _to_schema(record)


report_repository = ReportRepository()

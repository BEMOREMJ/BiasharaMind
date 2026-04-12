from sqlalchemy import select, update

from app.db.session import session_scope
from app.models.analysis import AnalysisRecord
from app.schemas.analysis import AnalysisCategoryScore, AnalysisSummaryRead, PriorityRecommendation


def _to_schema(record: AnalysisRecord) -> AnalysisSummaryRead:
    return AnalysisSummaryRead(
        id=record.id,
        assessment_id=record.assessment_id,
        overall_score=float(record.overall_score),
        category_scores=[
            AnalysisCategoryScore.model_validate(item) for item in record.category_scores or []
        ],
        top_strengths=list(record.top_strengths or []),
        top_risks=list(record.top_risks or []),
        top_priorities=[
            PriorityRecommendation.model_validate(item) for item in record.top_priorities or []
        ],
        created_at=record.created_at.isoformat(),
        model_version=record.model_version,
        workflow_version=record.workflow_version,
    )


class AnalysisRepository:
    """PostgreSQL-backed repository for saved analysis summaries."""

    def get(self, user_id: str) -> AnalysisSummaryRead | None:
        with session_scope() as session:
            record = session.scalar(
                select(AnalysisRecord)
                .where(AnalysisRecord.user_id == user_id)
                .where(AnalysisRecord.is_active.is_(True))
                .order_by(AnalysisRecord.created_at.desc())
                .limit(1)
            )
            if record is None:
                return None
            return _to_schema(record)

    def save(self, analysis: AnalysisSummaryRead, user_id: str) -> AnalysisSummaryRead:
        with session_scope() as session:
            session.execute(
                update(AnalysisRecord)
                .where(AnalysisRecord.user_id == user_id)
                .where(AnalysisRecord.is_active.is_(True))
                .values(is_active=False)
            )
            record = AnalysisRecord(
                id=analysis.id,
                user_id=user_id,
                assessment_id=analysis.assessment_id,
                overall_score=analysis.overall_score,
                category_scores=[item.model_dump(mode="json") for item in analysis.category_scores],
                top_strengths=analysis.top_strengths,
                top_risks=analysis.top_risks,
                top_priorities=[item.model_dump(mode="json") for item in analysis.top_priorities],
                model_version=analysis.model_version,
                workflow_version=analysis.workflow_version,
            )
            session.add(record)
            session.flush()
            session.refresh(record)
            return _to_schema(record)


analysis_repository = AnalysisRepository()

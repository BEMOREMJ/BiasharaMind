from sqlalchemy import select

from app.db.session import session_scope
from app.models.analysis_run import AnalysisRunRecord
from app.v2.schemas.diagnosis import (
    CriticalRiskRead,
    DiagnosisSummaryRead,
    IssueCandidateRead,
    PriorityRead,
    RoadmapInputPackageRead,
    WatchlistItemRead,
)
from app.v2.schemas.explainability import ExplainabilitySnapshot
from app.v2.schemas.lifecycle import AnalysisLifecycleState
from app.v2.schemas.meta import V2VersionMetadata
from app.v2.schemas.snapshots import TextInterpretationSnapshot
from app.v2.schemas.scoring import AnalysisRunRead, AnalysisScoreSummary


def _to_schema(record: AnalysisRunRecord) -> AnalysisRunRead:
    snapshot = record.snapshot_payload or {}
    return AnalysisRunRead(
        id=record.id,
        analysis_family=record.analysis_family,
        metadata=V2VersionMetadata.model_validate(snapshot.get("metadata", {})),
        lifecycle=AnalysisLifecycleState.model_validate(snapshot.get("lifecycle", {})),
        summary=AnalysisScoreSummary.model_validate(snapshot.get("deterministicScores", {})),
        critical_risks=[CriticalRiskRead.model_validate(item) for item in snapshot.get("criticalRisks", [])],
        diagnosis=DiagnosisSummaryRead.model_validate(snapshot.get("diagnosis", {})),
        issue_candidates=[IssueCandidateRead.model_validate(item) for item in snapshot.get("issueCandidates", [])],
        top_priorities=[PriorityRead.model_validate(item) for item in snapshot.get("topPriorities", [])],
        watchlist=[WatchlistItemRead.model_validate(item) for item in snapshot.get("watchlist", [])],
        roadmap_inputs=RoadmapInputPackageRead.model_validate(snapshot.get("roadmapInputs", {})),
        text_interpretation=TextInterpretationSnapshot.model_validate(snapshot.get("textInterpretation", {})),
        explainability=ExplainabilitySnapshot.model_validate(snapshot.get("explainability", {})),
        created_at=record.created_at.isoformat(),
    )


class AnalysisV2Repository:
    def get_latest(self, user_id: str) -> AnalysisRunRead | None:
        with session_scope() as session:
            record = session.scalar(
                select(AnalysisRunRecord)
                .where(AnalysisRunRecord.user_id == user_id)
                .where(AnalysisRunRecord.analysis_family == "v2_assessment")
                .order_by(AnalysisRunRecord.created_at.desc())
                .limit(1)
            )
            if record is None:
                return None
            return _to_schema(record)

    def create(self, record: AnalysisRunRecord) -> AnalysisRunRead:
        with session_scope() as session:
            session.add(record)
            session.flush()
            session.refresh(record)
            return _to_schema(record)


analysis_v2_repository = AnalysisV2Repository()

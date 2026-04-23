from sqlalchemy import select

from app.db.session import session_scope
from app.models.analysis_run import AnalysisRunRecord
from app.v2.schemas.lifecycle import FreshnessState, RerunReason


class AnalysisRunV2Repository:
    def mark_stale_due_to_profile_change(self, user_id: str) -> int:
        with session_scope() as session:
            records = list(
                session.scalars(
                    select(AnalysisRunRecord)
                    .where(AnalysisRunRecord.user_id == user_id)
                    .where(
                        AnalysisRunRecord.freshness_status.in_(
                            [FreshnessState.FRESH.value, FreshnessState.PROVISIONAL.value]
                        )
                    )
                )
            )

            for record in records:
                record.freshness_status = FreshnessState.STALE_DUE_TO_PROFILE_CHANGE.value
                record.rerun_required = True
                record.rerun_reason = RerunReason.PROFILE_CHANGED.value

            return len(records)


analysis_run_v2_repository = AnalysisRunV2Repository()

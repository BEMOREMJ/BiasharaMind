from typing import TYPE_CHECKING, Any

from app.v2.schemas.profile import (
    AnalysisImpactSummary,
    BusinessProfileV2Create,
    BusinessProfileV2Read,
    BusinessProfileV2SaveResponse,
    BusinessProfileV2Update,
    apply_business_profile_v2_update,
    create_business_profile_v2_read,
)

if TYPE_CHECKING:
    from app.v2.repositories.analysis_runs import AnalysisRunV2Repository
    from app.v2.repositories.business_profile import BusinessProfileV2Repository


class BusinessProfileV2Service:
    def __init__(
        self,
        profile_repository: "BusinessProfileV2Repository | Any" = None,
        analysis_run_repository: "AnalysisRunV2Repository | Any" = None,
    ) -> None:
        if profile_repository is None or analysis_run_repository is None:
            from app.v2.repositories.analysis_runs import analysis_run_v2_repository
            from app.v2.repositories.business_profile import business_profile_v2_repository

        self.profile_repository = profile_repository
        self.analysis_run_repository = analysis_run_repository
        if self.profile_repository is None:
            self.profile_repository = business_profile_v2_repository
        if self.analysis_run_repository is None:
            self.analysis_run_repository = analysis_run_v2_repository

    def get_profile(self, user_id: str) -> BusinessProfileV2Read | None:
        return self.profile_repository.get(user_id)

    def save_profile(
        self,
        payload: BusinessProfileV2Create | BusinessProfileV2Update,
        user_id: str,
    ) -> BusinessProfileV2SaveResponse:
        existing = self.profile_repository.get(user_id)
        if existing is None:
            profile = self.profile_repository.create(create_business_profile_v2_read(payload, user_id))
            return BusinessProfileV2SaveResponse(
                profile=profile,
                analysis_impact=AnalysisImpactSummary(
                    stale_analysis_runs=0,
                    rerun_required=False,
                ),
            )

        updated_profile = self.profile_repository.update(
            apply_business_profile_v2_update(existing, payload),
            user_id,
        )
        stale_count = self.analysis_run_repository.mark_stale_due_to_profile_change(user_id)
        return BusinessProfileV2SaveResponse(
            profile=updated_profile,
            analysis_impact=AnalysisImpactSummary(
                stale_analysis_runs=stale_count,
                rerun_required=stale_count > 0,
                message=(
                    "Your business context changed. Future V2 analysis should be rerun to reflect the latest profile."
                    if stale_count > 0
                    else None
                ),
            ),
        )


_business_profile_v2_service: BusinessProfileV2Service | None = None


def get_business_profile_v2_service() -> BusinessProfileV2Service:
    global _business_profile_v2_service
    if _business_profile_v2_service is None:
        _business_profile_v2_service = BusinessProfileV2Service()
    return _business_profile_v2_service

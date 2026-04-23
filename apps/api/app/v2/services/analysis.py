from __future__ import annotations

from types import SimpleNamespace
from typing import TYPE_CHECKING, Any
from uuid import uuid4

from app.v2.schemas.assessment import AssessmentRead
from app.v2.schemas.meta import CURRENT_V2_VERSION_METADATA
from app.v2.schemas.scoring import AnalysisRunRead
from app.v2.services.scoring import ScoreContext, run_deterministic_scoring

if TYPE_CHECKING:
    from app.v2.repositories.analysis import AnalysisV2Repository
    from app.v2.repositories.assessment import AssessmentV2Repository
    from app.v2.services.business_profile import BusinessProfileV2Service


class MissingSubmittedAssessmentError(ValueError):
    pass


def _question_view(question: dict[str, Any]) -> Any:
    payload = dict(question)
    payload["scale_key"] = question.get("scaleKey") or question.get("answerSpec", {}).get("scaleKey")
    if payload["scale_key"] is None:
        response_type = question.get("answerSpec", {}).get("responseType")
        if response_type == "number":
            payload["scale_key"] = "numeric_0_10"
    payload["question_type"] = question.get("questionType")
    payload["essential"] = question.get("essential", False)
    payload["scored"] = question.get("scored", False)
    payload["bucket"] = question.get("bucket")
    payload["question_id"] = question.get("questionId")
    return type("QuestionView", (), payload)()


class AnalysisV2Service:
    def __init__(
        self,
        analysis_repository: "AnalysisV2Repository | Any" = None,
        assessment_repository: "AssessmentV2Repository | Any" = None,
        business_profile_service: "BusinessProfileV2Service | Any" = None,
    ) -> None:
        if analysis_repository is None or assessment_repository is None or business_profile_service is None:
            from app.v2.repositories.analysis import analysis_v2_repository
            from app.v2.repositories.assessment import assessment_v2_repository
            from app.v2.services.business_profile import get_business_profile_v2_service

        self.analysis_repository = analysis_repository or analysis_v2_repository
        self.assessment_repository = assessment_repository or assessment_v2_repository
        self.business_profile_service = business_profile_service or get_business_profile_v2_service()

    def get_latest(self, user_id: str) -> AnalysisRunRead | None:
        return self.analysis_repository.get_latest(user_id)

    def _require_inputs(self, user_id: str) -> tuple[Any, AssessmentRead]:
        profile = self.business_profile_service.get_profile(user_id)
        if profile is None:
            raise MissingSubmittedAssessmentError("Complete the V2 business profile before running V2 analysis.")
        assessment = self.assessment_repository.get_latest_submitted(user_id)
        if assessment is None:
            raise MissingSubmittedAssessmentError("Submit the V2 assessment before running V2 analysis.")
        return profile, assessment

    def run_analysis(self, user_id: str) -> AnalysisRunRead:
        try:
            from app.models.analysis_run import AnalysisRunRecord
        except ModuleNotFoundError:
            AnalysisRunRecord = SimpleNamespace  # type: ignore[assignment]

        profile, assessment = self._require_inputs(user_id)
        snapshot = assessment.latest_definition_snapshot or {}
        section_titles = {
            section["sectionId"]: section["title"]
            for section in snapshot.get("sections", [])
            if section.get("isCore")
        }
        section_question_ids = {
            section["sectionId"]: [question["questionId"] for question in section.get("questions", [])]
            for section in snapshot.get("sections", [])
        }
        module_parent_map = {
            module["moduleId"]: module["parentSectionKey"]
            for module in snapshot.get("adaptiveModules", [])
            if module.get("moduleId") and module.get("parentSectionKey")
        }
        question_map = {
            question["questionId"]: _question_view(question)
            for section in snapshot.get("sections", [])
            for question in section.get("questions", [])
        }
        summary, explainability, lifecycle = run_deterministic_scoring(
            ScoreContext(
                answers=assessment.answers,
                question_map=question_map,
                section_titles=section_titles,
                module_parent_map=module_parent_map,
                section_question_ids=section_question_ids,
            )
        )
        metadata = CURRENT_V2_VERSION_METADATA.model_copy(
            update={
                "scoring_version": "v2.0.0-deterministic-foundation",
                "analysis_engine_version": "v2.0.0-scoring-foundation",
            }
        )
        payload = {
            "metadata": metadata.model_dump(mode="json", by_alias=True),
            "lifecycle": lifecycle.model_dump(mode="json", by_alias=True),
            "deterministicScores": summary.model_dump(mode="json", by_alias=True),
            "explainability": explainability.model_dump(mode="json", by_alias=True),
            "profileSnapshot": profile.model_dump(mode="json", by_alias=True),
            "assessmentSnapshot": assessment.model_dump(mode="json", by_alias=True),
        }
        record = AnalysisRunRecord(
            id=f"analysis_run_v2_{uuid4().hex}",
            user_id=user_id,
            business_profile_v2_id=profile.id,
            assessment_v2_id=assessment.id,
            analysis_family="v2_assessment",
            question_bank_version=metadata.question_bank_version,
            scoring_version=metadata.scoring_version,
            taxonomy_version=metadata.taxonomy_version,
            prompt_version=metadata.prompt_version,
            analysis_engine_version=metadata.analysis_engine_version,
            freshness_status=lifecycle.freshness_status.value,
            rerun_required=lifecycle.rerun_required,
            rerun_reason=lifecycle.rerun_reason.value if lifecycle.rerun_reason else None,
            ai_interpretation_status=lifecycle.ai_interpretation_status.value,
            snapshot_payload=payload,
        )
        return self.analysis_repository.create(record)


_analysis_v2_service: AnalysisV2Service | None = None


def get_analysis_v2_service() -> AnalysisV2Service:
    global _analysis_v2_service
    if _analysis_v2_service is None:
        _analysis_v2_service = AnalysisV2Service()
    return _analysis_v2_service

from datetime import UTC, datetime
from typing import TYPE_CHECKING, Any
from uuid import uuid4

from app.v2.config import ADAPTIVE_MODULE_REGISTRY, CORE_SECTION_REGISTRY, SCALE_LIBRARY
from app.v2.schemas.assessment import (
    AdaptiveModuleDefinitionRead,
    AnswerValueOption,
    AssessmentAnswerPayload,
    AssessmentAnswerRead,
    AssessmentDefinitionRead,
    AssessmentQuestionDefinition,
    AssessmentRead,
    AssessmentSaveResponse,
    AssessmentSectionDefinition,
    AssessmentStatus,
    AssessmentWritePayload,
    QuestionAnswerSpec,
    QuestionApplicability,
    ResponseKind,
)
from app.v2.schemas.meta import CURRENT_V2_VERSION_METADATA
from app.v2.schemas.profile import AnalysisImpactSummary, BusinessProfileV2Read

if TYPE_CHECKING:
    from app.v2.repositories.analysis_runs import AnalysisRunV2Repository
    from app.v2.repositories.assessment import AssessmentV2Repository
    from app.v2.services.business_profile import BusinessProfileV2Service


class MissingBusinessProfileError(ValueError):
    pass


def _count_total_questions(snapshot: dict[str, Any] | None) -> int:
    if not snapshot:
        return 0
    return sum(len(section.get("questions", [])) for section in snapshot.get("sections", []))


class AssessmentV2Service:
    def __init__(
        self,
        assessment_repository: "AssessmentV2Repository | Any" = None,
        analysis_run_repository: "AnalysisRunV2Repository | Any" = None,
        business_profile_service: "BusinessProfileV2Service | Any" = None,
    ) -> None:
        if assessment_repository is None or analysis_run_repository is None or business_profile_service is None:
            from app.v2.repositories.analysis_runs import analysis_run_v2_repository
            from app.v2.repositories.assessment import assessment_v2_repository
            from app.v2.services.business_profile import get_business_profile_v2_service

        self.assessment_repository = assessment_repository or assessment_v2_repository
        self.analysis_run_repository = analysis_run_repository or analysis_run_v2_repository
        self.business_profile_service = business_profile_service or get_business_profile_v2_service()
        self.scale_map = {scale.key: scale for scale in SCALE_LIBRARY}

    def _require_profile(self, user_id: str) -> BusinessProfileV2Read:
        profile = self.business_profile_service.get_profile(user_id)
        if profile is None:
            raise MissingBusinessProfileError(
                "Complete the V2 business profile before starting the V2 assessment."
            )
        return profile

    def select_applicable_modules(self, profile: BusinessProfileV2Read) -> list[Any]:
        profile_values = profile.model_dump()
        selected = []
        for module in ADAPTIVE_MODULE_REGISTRY:
            field_value = profile_values.get(module.trigger_field)
            if isinstance(field_value, list):
                if any(item in module.trigger_values for item in field_value):
                    selected.append(module)
            elif field_value in module.trigger_values:
                selected.append(module)
        return selected

    def _build_answer_spec(self, question: Any) -> QuestionAnswerSpec:
        scale = self.scale_map.get(question.scale_key) if question.scale_key else None
        options = []
        min_value = None
        max_value = None
        step = None

        if scale is not None:
            options = [AnswerValueOption(value=option.value, label=option.label) for option in scale.options]
            min_value = scale.min_value
            max_value = scale.max_value
            step = scale.step

        return QuestionAnswerSpec(
            response_type=question.input_type,
            options=options,
            min_value=min_value,
            max_value=max_value,
            step=step,
            allow_unknown=question.allow_unknown,
            allow_prefer_not_to_say=question.allow_prefer_not_to_say,
            max_length=question.max_length,
            multi_select_max_items=question.multi_select_max_items,
        )

    def build_definition(self, user_id: str) -> AssessmentDefinitionRead:
        profile = self._require_profile(user_id)
        selected_modules = self.select_applicable_modules(profile)
        sections: list[AssessmentSectionDefinition] = []
        order_index = 1

        for section in CORE_SECTION_REGISTRY:
            questions = [
                AssessmentQuestionDefinition(
                    question_id=question.key,
                    prompt=question.prompt,
                    question_type=question.input_type,
                    scale_key=question.scale_key,
                    interpretation_enabled=question.interpretation_enabled,
                    answer_spec=self._build_answer_spec(question),
                    essential=question.essential,
                    scored=question.scored,
                    bucket=question.bucket,
                    help_text=question.help_text,
                    order=order_index + index,
                    applicability=QuestionApplicability(section_id=section.key),
                    tags=question.tags,
                )
                for index, question in enumerate(section.questions)
            ]
            order_index += len(questions)
            sections.append(
                AssessmentSectionDefinition(
                    section_id=section.key,
                    title=section.label,
                    description=section.description,
                    order=section.order,
                    is_core=True,
                    questions=questions,
                )
            )

        adaptive_modules = []
        next_order = len(sections) + 1
        for module in selected_modules:
            module_questions = [
                AssessmentQuestionDefinition(
                    question_id=question.key,
                    prompt=question.prompt,
                    question_type=question.input_type,
                    scale_key=question.scale_key,
                    interpretation_enabled=question.interpretation_enabled,
                    answer_spec=self._build_answer_spec(question),
                    essential=question.essential,
                    scored=question.scored,
                    bucket=question.bucket,
                    help_text=question.help_text,
                    order=order_index + index,
                    applicability=QuestionApplicability(
                        section_id=module.key,
                        module_id=module.key,
                        trigger_field=module.trigger_field,
                        trigger_values=module.trigger_values,
                    ),
                    tags=question.tags,
                )
                for index, question in enumerate(module.questions)
            ]
            order_index += len(module_questions)
            sections.append(
                AssessmentSectionDefinition(
                    section_id=module.key,
                    title=module.label,
                    description=module.description,
                    order=next_order,
                    is_core=False,
                    module_id=module.key,
                    questions=module_questions,
                )
            )
            adaptive_modules.append(
                AdaptiveModuleDefinitionRead(
                    module_id=module.key,
                    title=module.label,
                    description=module.description,
                    trigger_field=module.trigger_field,
                    trigger_values=module.trigger_values,
                    parent_section_key=module.parent_section_key,
                    question_ids=[question.key for question in module.questions],
                )
            )
            next_order += 1

        return AssessmentDefinitionRead(
            business_profile_v2_id=profile.id,
            question_bank_version=CURRENT_V2_VERSION_METADATA.question_bank_version,
            sections=sections,
            adaptive_modules=adaptive_modules,
            total_questions=sum(len(section.questions) for section in sections),
        )

    def get_assessment(self, user_id: str) -> AssessmentRead | None:
        return self.assessment_repository.get_latest(user_id)

    def _question_map(self, definition: AssessmentDefinitionRead) -> dict[str, AssessmentQuestionDefinition]:
        return {
            question.question_id: question
            for section in definition.sections
            for question in section.questions
        }

    def normalize_answers(
        self,
        payload: AssessmentWritePayload,
        definition: AssessmentDefinitionRead,
    ) -> list[AssessmentAnswerRead]:
        question_map = self._question_map(definition)
        normalized_answers: list[AssessmentAnswerRead] = []
        seen_question_ids: set[str] = set()

        for order_index, answer in enumerate(payload.answers):
            if answer.question_id in seen_question_ids:
                raise ValueError(f"Duplicate answer provided for {answer.question_id}")
            seen_question_ids.add(answer.question_id)

            question = question_map.get(answer.question_id)
            if question is None:
                raise ValueError(f"Unknown question_id: {answer.question_id}")
            if answer.answer_type != question.question_type:
                raise ValueError(f"answer_type mismatch for {answer.question_id}")

            normalized_value = self._normalize_answer_value(answer, question)
            normalized_answers.append(
                AssessmentAnswerRead(
                    question_id=question.question_id,
                    section_id=question.applicability.section_id,
                    module_id=question.applicability.module_id,
                    answer_type=question.question_type,
                    response_kind=answer.response_kind,
                    value=normalized_value,
                    is_sufficient_answer=answer.response_kind == ResponseKind.ANSWERED,
                    order_index=order_index,
                )
            )

        return normalized_answers

    def _normalize_answer_value(
        self,
        answer: AssessmentAnswerPayload,
        question: AssessmentQuestionDefinition,
    ) -> str | int | float | list[str] | None:
        if answer.response_kind == ResponseKind.UNKNOWN:
            if not question.answer_spec.allow_unknown:
                raise ValueError(f"{question.question_id} does not allow unknown responses")
            return None
        if answer.response_kind == ResponseKind.PREFER_NOT_TO_SAY:
            if not question.answer_spec.allow_prefer_not_to_say:
                raise ValueError(f"{question.question_id} does not allow prefer_not_to_say")
            return None

        value = answer.value
        if question.question_type == "select":
            if not isinstance(value, str):
                raise ValueError(f"{question.question_id} requires a string selection")
            allowed_values = {option.value for option in question.answer_spec.options}
            if value not in allowed_values:
                raise ValueError(f"{question.question_id} must use a supported option")
            return value
        if question.question_type == "multiselect":
            if not isinstance(value, list) or not all(isinstance(item, str) for item in value):
                raise ValueError(f"{question.question_id} requires a list of selected values")
            allowed_values = {option.value for option in question.answer_spec.options}
            cleaned: list[str] = []
            for item in value:
                normalized = item.strip()
                if normalized not in allowed_values:
                    raise ValueError(f"{question.question_id} includes an unsupported selection")
                if normalized not in cleaned:
                    cleaned.append(normalized)
            max_items = question.answer_spec.multi_select_max_items or len(allowed_values)
            if len(cleaned) > max_items:
                raise ValueError(f"{question.question_id} exceeds the allowed selection count")
            return cleaned
        if question.question_type == "number":
            if not isinstance(value, (int, float)):
                raise ValueError(f"{question.question_id} requires a numeric value")
            numeric_value = float(value)
            if question.answer_spec.min_value is not None and numeric_value < question.answer_spec.min_value:
                raise ValueError(f"{question.question_id} is below the minimum allowed value")
            if question.answer_spec.max_value is not None and numeric_value > question.answer_spec.max_value:
                raise ValueError(f"{question.question_id} is above the maximum allowed value")
            return round(numeric_value, 2)
        if question.question_type in {"text", "textarea"}:
            if not isinstance(value, str) or not value.strip():
                raise ValueError(f"{question.question_id} requires text")
            max_length = question.answer_spec.max_length or 4000
            normalized_text = value.strip()
            if len(normalized_text) > max_length:
                raise ValueError(f"{question.question_id} exceeds the maximum allowed length")
            return normalized_text
        raise ValueError(f"Unsupported question type for {question.question_id}")

    def _build_assessment_record(
        self,
        user_id: str,
        definition: AssessmentDefinitionRead,
        answers: list[AssessmentAnswerRead],
        status: AssessmentStatus,
        existing: AssessmentRead | None,
    ) -> AssessmentRead:
        total_questions = definition.total_questions
        answered_count = len([answer for answer in answers if answer.is_sufficient_answer])
        latest_snapshot = definition.model_dump(mode="json", by_alias=True)
        started_at = existing.started_at if existing else datetime.now(UTC).isoformat()
        submitted_at = datetime.now(UTC).isoformat() if status == AssessmentStatus.SUBMITTED else None
        return AssessmentRead(
            id=existing.id if existing else f"assessment_v2_{uuid4().hex}",
            business_profile_v2_id=definition.business_profile_v2_id,
            question_bank_version=definition.question_bank_version,
            status=status,
            completeness_hint=f"answered_{answered_count}_of_{total_questions}",
            latest_definition_snapshot=latest_snapshot,
            started_at=started_at,
            submitted_at=submitted_at,
            answers=answers,
        )

    def save_assessment(self, payload: AssessmentWritePayload, user_id: str) -> AssessmentSaveResponse:
        definition = self.build_definition(user_id)
        normalized_answers = self.normalize_answers(payload, definition)
        existing = self.assessment_repository.get_latest(user_id)
        assessment = self._build_assessment_record(
            user_id=user_id,
            definition=definition,
            answers=normalized_answers,
            status=AssessmentStatus.DRAFT,
            existing=existing,
        )
        saved = self.assessment_repository.save(assessment, user_id)
        stale_count = self.analysis_run_repository.mark_stale_due_to_assessment_change(user_id) if existing else 0
        return AssessmentSaveResponse(
            assessment=saved,
            analysis_impact=AnalysisImpactSummary(
                stale_analysis_runs=stale_count,
                rerun_required=stale_count > 0,
                message=(
                    "Your assessment changed. Future V2 analysis should be rerun to reflect the latest answers."
                    if stale_count > 0
                    else None
                ),
            ),
        )

    def submit_assessment(self, payload: AssessmentWritePayload, user_id: str) -> AssessmentSaveResponse:
        definition = self.build_definition(user_id)
        normalized_answers = self.normalize_answers(payload, definition)
        existing = self.assessment_repository.get_latest(user_id)
        assessment = self._build_assessment_record(
            user_id=user_id,
            definition=definition,
            answers=normalized_answers,
            status=AssessmentStatus.SUBMITTED,
            existing=existing,
        )
        saved = self.assessment_repository.save(assessment, user_id)
        stale_count = self.analysis_run_repository.mark_stale_due_to_assessment_change(user_id) if existing else 0
        return AssessmentSaveResponse(
            assessment=saved,
            analysis_impact=AnalysisImpactSummary(
                stale_analysis_runs=stale_count,
                rerun_required=stale_count > 0,
                message=(
                    "Your assessment changed. Future V2 analysis should be rerun to reflect the latest answers."
                    if stale_count > 0
                    else None
                ),
            ),
        )


_assessment_v2_service: AssessmentV2Service | None = None


def get_assessment_v2_service() -> AssessmentV2Service:
    global _assessment_v2_service
    if _assessment_v2_service is None:
        _assessment_v2_service = AssessmentV2Service()
    return _assessment_v2_service

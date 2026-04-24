from datetime import UTC, datetime
from enum import StrEnum
from typing import Any
from uuid import uuid4

from pydantic import Field, model_validator

from app.v2.common import V2BaseModel
from app.v2.schemas.profile import AnalysisImpactSummary


class AssessmentStatus(StrEnum):
    DRAFT = "draft"
    SUBMITTED = "submitted"


class ResponseKind(StrEnum):
    ANSWERED = "answered"
    UNKNOWN = "unknown"
    PREFER_NOT_TO_SAY = "prefer_not_to_say"


class AnswerValueOption(V2BaseModel):
    value: str = Field(min_length=1, max_length=64)
    label: str = Field(min_length=1, max_length=120)


class QuestionAnswerSpec(V2BaseModel):
    response_type: str = Field(min_length=1, max_length=32)
    options: list[AnswerValueOption] = Field(default_factory=list, max_length=20)
    min_value: float | None = Field(default=None, ge=0, le=100)
    max_value: float | None = Field(default=None, ge=0, le=100)
    step: float | None = Field(default=None, gt=0, le=100)
    allow_unknown: bool = False
    allow_prefer_not_to_say: bool = False
    max_length: int | None = Field(default=None, ge=1, le=4000)
    multi_select_max_items: int | None = Field(default=None, ge=1, le=12)


class QuestionApplicability(V2BaseModel):
    section_id: str = Field(min_length=2, max_length=64)
    module_id: str | None = Field(default=None, max_length=64)
    trigger_field: str | None = Field(default=None, max_length=64)
    trigger_values: list[str] = Field(default_factory=list, max_length=20)


class AssessmentQuestionDefinition(V2BaseModel):
    question_id: str = Field(min_length=2, max_length=64)
    prompt: str = Field(min_length=1, max_length=320)
    question_type: str = Field(min_length=1, max_length=32)
    scale_key: str | None = Field(default=None, max_length=64)
    interpretation_enabled: bool = False
    answer_spec: QuestionAnswerSpec
    essential: bool = False
    scored: bool = True
    bucket: str = Field(min_length=1, max_length=64)
    help_text: str | None = Field(default=None, max_length=240)
    order: int = Field(ge=1, le=200)
    applicability: QuestionApplicability
    tags: list[str] = Field(default_factory=list, max_length=10)


class AssessmentSectionDefinition(V2BaseModel):
    section_id: str = Field(min_length=2, max_length=64)
    title: str = Field(min_length=1, max_length=120)
    description: str = Field(min_length=1, max_length=280)
    order: int = Field(ge=1, le=20)
    is_core: bool = True
    module_id: str | None = Field(default=None, max_length=64)
    questions: list[AssessmentQuestionDefinition] = Field(default_factory=list, max_length=40)


class AdaptiveModuleDefinitionRead(V2BaseModel):
    module_id: str = Field(min_length=2, max_length=64)
    title: str = Field(min_length=1, max_length=120)
    description: str = Field(min_length=1, max_length=280)
    trigger_field: str = Field(min_length=2, max_length=64)
    trigger_values: list[str] = Field(min_length=1, max_length=20)
    parent_section_key: str = Field(min_length=2, max_length=64)
    question_ids: list[str] = Field(default_factory=list, max_length=20)


class AssessmentDefinitionRead(V2BaseModel):
    business_profile_v2_id: str = Field(min_length=2, max_length=64)
    question_bank_version: str = Field(min_length=1, max_length=64)
    sections: list[AssessmentSectionDefinition] = Field(min_length=1, max_length=20)
    adaptive_modules: list[AdaptiveModuleDefinitionRead] = Field(default_factory=list, max_length=10)
    total_questions: int = Field(ge=1, le=200)


class AssessmentAnswerPayload(V2BaseModel):
    question_id: str = Field(min_length=2, max_length=64)
    answer_type: str = Field(min_length=1, max_length=32)
    response_kind: ResponseKind = ResponseKind.ANSWERED
    value: str | int | float | list[str] | None = None

    @model_validator(mode="after")
    def validate_payload(self) -> "AssessmentAnswerPayload":
        if self.response_kind == ResponseKind.ANSWERED and self.value is None:
            raise ValueError("answered responses require a value")
        if self.response_kind != ResponseKind.ANSWERED and self.value is not None:
            raise ValueError("unknown or prefer_not_to_say responses cannot include a value")
        return self


class AssessmentWritePayload(V2BaseModel):
    answers: list[AssessmentAnswerPayload] = Field(default_factory=list, max_length=200)


class AssessmentAnswerRead(V2BaseModel):
    question_id: str = Field(min_length=2, max_length=64)
    section_id: str = Field(min_length=2, max_length=64)
    module_id: str | None = Field(default=None, max_length=64)
    answer_type: str = Field(min_length=1, max_length=32)
    response_kind: ResponseKind
    value: str | int | float | list[str] | None = None
    is_sufficient_answer: bool | None = None
    order_index: int | None = Field(default=None, ge=0, le=500)


class AssessmentRead(V2BaseModel):
    id: str
    business_profile_v2_id: str | None = Field(default=None, max_length=64)
    question_bank_version: str = Field(min_length=1, max_length=64)
    status: AssessmentStatus
    completeness_hint: str | None = Field(default=None, max_length=64)
    latest_definition_snapshot: dict[str, Any] | None = None
    started_at: str
    submitted_at: str | None = None
    answers: list[AssessmentAnswerRead] = Field(default_factory=list, max_length=200)


class AssessmentSaveResponse(V2BaseModel):
    assessment: AssessmentRead
    analysis_impact: AnalysisImpactSummary


def build_completeness_hint(answered_count: int, total_questions: int) -> str:
    return f"answered_{answered_count}_of_{total_questions}"


def create_assessment_read(
    business_profile_v2_id: str,
    question_bank_version: str,
    latest_definition_snapshot: dict[str, Any],
    answers: list[AssessmentAnswerRead],
    status: AssessmentStatus,
) -> AssessmentRead:
    timestamp = datetime.now(UTC).isoformat()
    answered_count = len([answer for answer in answers if answer.is_sufficient_answer])
    return AssessmentRead(
        id=f"assessment_v2_{uuid4().hex}",
        business_profile_v2_id=business_profile_v2_id,
        question_bank_version=question_bank_version,
        status=status,
        completeness_hint=build_completeness_hint(answered_count, max(len(latest_definition_snapshot.get("sections", [])), 1)),
        latest_definition_snapshot=latest_definition_snapshot,
        started_at=timestamp,
        submitted_at=timestamp if status == AssessmentStatus.SUBMITTED else None,
        answers=answers,
    )

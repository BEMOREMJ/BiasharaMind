from pydantic import Field

from app.v2.common import V2BaseModel
from app.v2.schemas.explainability import ExplainabilitySnapshot
from app.v2.schemas.interpretation import TextInterpretationInput, TextInterpretationOutput
from app.v2.schemas.lifecycle import AIInterpretationStatus, AnalysisLifecycleState
from app.v2.schemas.meta import V2VersionMetadata


class SourceEntityReferences(V2BaseModel):
    analysis_run_id: str | None = Field(default=None, max_length=64)
    user_id: str | None = Field(default=None, max_length=128)
    business_profile_id: str | None = Field(default=None, max_length=64)
    assessment_id: str | None = Field(default=None, max_length=64)


class BusinessProfileSnapshot(V2BaseModel):
    values: dict[str, str | int | list[str]] = Field(default_factory=dict)


class AssessmentAnswerSnapshot(V2BaseModel):
    question_key: str = Field(min_length=2, max_length=64)
    section_key: str = Field(min_length=2, max_length=64)
    answer_type: str = Field(min_length=1, max_length=32)
    value: str | int | float | list[str]


class AssessmentSubmissionSnapshot(V2BaseModel):
    sections: list[str] = Field(default_factory=list, max_length=20)
    answers: list[AssessmentAnswerSnapshot] = Field(default_factory=list, max_length=200)


class TextInterpretationSnapshot(V2BaseModel):
    status: AIInterpretationStatus = AIInterpretationStatus.NOT_REQUESTED
    prompt_version: str | None = Field(default=None, max_length=64)
    provider_name: str | None = Field(default=None, max_length=64)
    inputs: list[TextInterpretationInput] = Field(default_factory=list, max_length=200)
    outputs: list[TextInterpretationOutput] = Field(default_factory=list, max_length=200)


class PlaceholderScorePayload(V2BaseModel):
    overall_score: float | None = Field(default=None, ge=0, le=100)
    section_scores: list[dict[str, str | float]] = Field(default_factory=list, max_length=20)


class AnalysisSnapshotEnvelope(V2BaseModel):
    metadata: V2VersionMetadata
    lifecycle: AnalysisLifecycleState
    source_entities: SourceEntityReferences = Field(default_factory=SourceEntityReferences)
    business_profile: BusinessProfileSnapshot = Field(default_factory=BusinessProfileSnapshot)
    assessment_submission: AssessmentSubmissionSnapshot = Field(default_factory=AssessmentSubmissionSnapshot)
    text_interpretation: TextInterpretationSnapshot = Field(default_factory=TextInterpretationSnapshot)
    explainability: ExplainabilitySnapshot = Field(default_factory=ExplainabilitySnapshot)
    deterministic_scores: PlaceholderScorePayload | None = None
    issue_summary: list[dict[str, str]] | None = None
    priorities: list[dict[str, str]] | None = None
    roadmap_inputs: list[dict[str, str]] | None = None

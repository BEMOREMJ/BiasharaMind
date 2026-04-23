from enum import StrEnum

from pydantic import Field

from app.v2.common import V2BaseModel
from app.v2.schemas.explainability import ExplainabilitySnapshot
from app.v2.schemas.lifecycle import AnalysisLifecycleState
from app.v2.schemas.meta import V2VersionMetadata


class HealthStatus(StrEnum):
    STRONG_AND_CONTROLLED = "strong_and_controlled"
    STABLE_BUT_CONSTRAINED = "stable_but_constrained"
    VULNERABLE = "vulnerable"
    FRAGILE = "fragile"
    CRITICAL = "critical"


class CoverageLabel(StrEnum):
    HIGH = "high_coverage"
    GOOD = "good_coverage"
    PARTIAL = "partial_coverage"
    LOW = "low_coverage"


class ConfidenceLabel(StrEnum):
    HIGH = "high_confidence"
    MODERATE = "moderate_confidence"
    LOW = "low_confidence"


class BucketScore(V2BaseModel):
    bucket: str = Field(min_length=1, max_length=32)
    score: float = Field(ge=0, le=100)
    contributing_question_count: int = Field(ge=0, le=100)


class SectionScore(V2BaseModel):
    section_id: str = Field(min_length=2, max_length=64)
    title: str = Field(min_length=1, max_length=120)
    score: float = Field(ge=0, le=100)
    bucket_scores: list[BucketScore] = Field(default_factory=list, max_length=3)
    completeness: float = Field(ge=0, le=100)
    completeness_label: CoverageLabel
    evidence_confidence: float = Field(ge=0, le=100)
    module_contribution_score: float | None = Field(default=None, ge=0, le=100)
    module_contribution_weight: float | None = Field(default=None, ge=0, le=1)


class CompletenessSummary(V2BaseModel):
    overall: float = Field(ge=0, le=100)
    label: CoverageLabel
    essential_answered_sufficiently: int = Field(ge=0, le=500)
    essential_applicable: int = Field(ge=0, le=500)
    optional_answered_sufficiently: int = Field(ge=0, le=500)
    optional_applicable: int = Field(ge=0, le=500)


class EvidenceConfidenceSummary(V2BaseModel):
    score: float = Field(ge=0, le=100)
    label: ConfidenceLabel
    specificity: float = Field(ge=0, le=100)
    quantification: float = Field(ge=0, le=100)
    internal_consistency: float = Field(ge=0, le=100)
    corroboration: float = Field(ge=0, le=100)
    key_limitations: list[str] = Field(default_factory=list, max_length=20)


class StatusCapResult(V2BaseModel):
    code: str = Field(min_length=1, max_length=64)
    label: str = Field(min_length=1, max_length=160)
    capped_status: HealthStatus
    reason: str = Field(min_length=1, max_length=320)


class AnalysisScoreSummary(V2BaseModel):
    overall_health_score: float = Field(ge=0, le=100)
    overall_status: HealthStatus
    section_scores: list[SectionScore] = Field(default_factory=list, max_length=20)
    completeness: CompletenessSummary
    evidence_confidence: EvidenceConfidenceSummary
    active_critical_risk_count: int = Field(ge=0, le=100)
    caps_applied: list[StatusCapResult] = Field(default_factory=list, max_length=10)


class AnalysisRunRead(V2BaseModel):
    id: str
    analysis_family: str = Field(min_length=1, max_length=64)
    metadata: V2VersionMetadata
    lifecycle: AnalysisLifecycleState
    summary: AnalysisScoreSummary
    explainability: ExplainabilitySnapshot
    created_at: str

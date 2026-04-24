from enum import StrEnum
from typing import Any

from pydantic import Field

from app.v2.common import V2BaseModel


class IssueTag(V2BaseModel):
    code: str = Field(min_length=1, max_length=64)
    label: str = Field(min_length=1, max_length=120)
    confidence: float = Field(ge=0, le=1)


class RootCauseTag(V2BaseModel):
    code: str = Field(min_length=1, max_length=64)
    label: str = Field(min_length=1, max_length=120)
    confidence: float = Field(ge=0, le=1)


class ContradictionSeverity(StrEnum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


class ContradictionFlag(V2BaseModel):
    code: str = Field(min_length=1, max_length=64)
    detail: str = Field(min_length=1, max_length=320)
    severity: ContradictionSeverity
    source_refs: list[str] = Field(default_factory=list, max_length=10)


class EvidenceSpecificity(StrEnum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


class EvidenceStrength(StrEnum):
    WEAK = "weak"
    MIXED = "mixed"
    STRONG = "strong"


class InterpretationConfidence(StrEnum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


class SeverityHint(StrEnum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class TextInterpretationInput(V2BaseModel):
    question_key: str = Field(min_length=2, max_length=64)
    section_key: str = Field(min_length=2, max_length=64)
    answer_text: str = Field(min_length=1, max_length=4000)
    business_profile_context: dict[str, Any] = Field(default_factory=dict)
    source_ref: str | None = Field(default=None, max_length=120)


class InterpretationFallbackResult(V2BaseModel):
    used: bool = False
    reason: str | None = Field(default=None, max_length=200)
    partial: bool = False
    recoverable: bool = True


class TextInterpretationOutput(V2BaseModel):
    question_key: str = Field(min_length=2, max_length=64)
    section_key: str = Field(min_length=2, max_length=64)
    summary: str | None = Field(default=None, max_length=500)
    issue_tags: list[IssueTag] = Field(default_factory=list, max_length=10)
    root_cause_tags: list[RootCauseTag] = Field(default_factory=list, max_length=10)
    affected_dimensions: list[str] = Field(default_factory=list, max_length=10)
    severity_hint: SeverityHint | None = None
    contradiction_flags: list[ContradictionFlag] = Field(default_factory=list, max_length=10)
    evidence_specificity: EvidenceSpecificity | None = None
    evidence_strength: EvidenceStrength | None = None
    interpretation_confidence: InterpretationConfidence | None = None
    evidence_snippets: list[str] = Field(default_factory=list, max_length=5)
    fallback: InterpretationFallbackResult = Field(default_factory=InterpretationFallbackResult)

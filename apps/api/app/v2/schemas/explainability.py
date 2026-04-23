from pydantic import Field

from app.v2.common import V2BaseModel


class ScoreDriver(V2BaseModel):
    code: str = Field(min_length=1, max_length=64)
    label: str = Field(min_length=1, max_length=140)
    direction: str = Field(min_length=1, max_length=20)
    detail: str = Field(min_length=1, max_length=320)
    evidence_refs: list[str] = Field(default_factory=list, max_length=10)


class AppliedCap(V2BaseModel):
    code: str = Field(min_length=1, max_length=64)
    label: str = Field(min_length=1, max_length=140)
    reason: str = Field(min_length=1, max_length=320)
    capped_to: float | None = Field(default=None, ge=0, le=100)


class EvidenceGap(V2BaseModel):
    area: str = Field(min_length=1, max_length=140)
    detail: str = Field(min_length=1, max_length=320)
    severity: str = Field(min_length=1, max_length=20)


class ConfidenceLimitation(V2BaseModel):
    code: str = Field(min_length=1, max_length=64)
    detail: str = Field(min_length=1, max_length=320)
    impact: str = Field(min_length=1, max_length=200)


class PriorityRationale(V2BaseModel):
    priority_code: str = Field(min_length=1, max_length=64)
    summary: str = Field(min_length=1, max_length=320)
    contributing_issue_codes: list[str] = Field(default_factory=list, max_length=10)
    contributing_risk_codes: list[str] = Field(default_factory=list, max_length=10)


class WatchlistRationale(V2BaseModel):
    watchlist_code: str = Field(min_length=1, max_length=64)
    summary: str = Field(min_length=1, max_length=320)
    trigger_condition: str = Field(min_length=1, max_length=200)


class ExplainabilitySnapshot(V2BaseModel):
    score_drivers: list[ScoreDriver] = Field(default_factory=list, max_length=20)
    caps_applied: list[AppliedCap] = Field(default_factory=list, max_length=20)
    missing_or_weak_evidence: list[EvidenceGap] = Field(default_factory=list, max_length=20)
    confidence_limitations: list[ConfidenceLimitation] = Field(default_factory=list, max_length=20)
    priority_rationales: list[PriorityRationale] = Field(default_factory=list, max_length=20)
    watchlist_rationales: list[WatchlistRationale] = Field(default_factory=list, max_length=20)

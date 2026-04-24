from pydantic import Field

from app.v2.common import V2BaseModel


class CriticalRiskRead(V2BaseModel):
    code: str = Field(min_length=2, max_length=64)
    title: str = Field(min_length=1, max_length=160)
    severity: str = Field(min_length=1, max_length=32)
    evidence_question_ids: list[str] = Field(default_factory=list, max_length=20)
    evidence_summary: str = Field(min_length=1, max_length=320)
    recommended_action_families: list[str] = Field(default_factory=list, max_length=10)


class IssueCandidateRead(V2BaseModel):
    issue_code: str = Field(min_length=2, max_length=64)
    title: str = Field(min_length=1, max_length=160)
    dimension: str = Field(min_length=1, max_length=64)
    evidence_question_ids: list[str] = Field(default_factory=list, max_length=20)
    evidence_summary: str = Field(min_length=1, max_length=400)
    severity_score: float = Field(ge=0, le=100)
    urgency_score: float = Field(ge=0, le=100)
    impact_score: float = Field(ge=0, le=100)
    feasibility_score: float = Field(ge=0, le=100)
    leverage_score: float = Field(ge=0, le=100)
    confidence_score: float = Field(ge=0, le=100)
    critical_risk_links: list[str] = Field(default_factory=list, max_length=10)
    recommended_action_family: str = Field(min_length=1, max_length=64)
    dependencies: list[str] = Field(default_factory=list, max_length=10)
    goal_fit_adjustment: float = Field(ge=0.8, le=1.2)
    priority_score: float = Field(ge=0, le=100)
    adjusted_priority_score: float = Field(ge=0, le=120)


class PriorityRead(V2BaseModel):
    issue_code: str = Field(min_length=2, max_length=64)
    title: str = Field(min_length=1, max_length=160)
    recommended_action_family: str = Field(min_length=1, max_length=64)
    adjusted_priority_score: float = Field(ge=0, le=120)
    why_selected: str = Field(min_length=1, max_length=400)
    sequencing_notes: list[str] = Field(default_factory=list, max_length=8)
    dependencies: list[str] = Field(default_factory=list, max_length=10)
    critical_risk_links: list[str] = Field(default_factory=list, max_length=10)
    suggested_success_metrics: list[str] = Field(default_factory=list, max_length=6)


class WatchlistItemRead(V2BaseModel):
    issue_code: str = Field(min_length=2, max_length=64)
    title: str = Field(min_length=1, max_length=160)
    recommended_action_family: str = Field(min_length=1, max_length=64)
    adjusted_priority_score: float = Field(ge=0, le=120)
    watchlist_reason: str = Field(min_length=1, max_length=320)
    critical_risk_links: list[str] = Field(default_factory=list, max_length=10)


class DiagnosisSummaryRead(V2BaseModel):
    strongest_areas: list[str] = Field(default_factory=list, max_length=3)
    weakest_areas: list[str] = Field(default_factory=list, max_length=3)
    primary_bottleneck: str | None = Field(default=None, max_length=160)
    top_constraints: list[str] = Field(default_factory=list, max_length=5)
    root_cause_patterns: list[str] = Field(default_factory=list, max_length=5)


class RoadmapInputItemRead(V2BaseModel):
    issue_code: str = Field(min_length=2, max_length=64)
    action_family: str = Field(min_length=1, max_length=64)
    dependencies: list[str] = Field(default_factory=list, max_length=10)
    feasibility_context: str = Field(min_length=1, max_length=320)
    suggested_success_metrics: list[str] = Field(default_factory=list, max_length=6)
    sequencing_notes: list[str] = Field(default_factory=list, max_length=8)


class RoadmapInputPackageRead(V2BaseModel):
    selected_action_families: list[str] = Field(default_factory=list, max_length=10)
    dependencies: list[str] = Field(default_factory=list, max_length=20)
    feasibility_context: list[str] = Field(default_factory=list, max_length=10)
    suggested_success_metrics: list[str] = Field(default_factory=list, max_length=12)
    sequencing_notes: list[str] = Field(default_factory=list, max_length=12)
    items: list[RoadmapInputItemRead] = Field(default_factory=list, max_length=5)

from enum import StrEnum

from pydantic import Field

from app.v2.common import V2BaseModel


class FreshnessState(StrEnum):
    FRESH = "fresh"
    PROVISIONAL = "provisional"
    STALE_DUE_TO_PROFILE_CHANGE = "stale_due_to_profile_change"
    STALE_DUE_TO_ASSESSMENT_CHANGE = "stale_due_to_assessment_change"
    STALE_DUE_TO_CONFIG_CHANGE = "stale_due_to_config_change"
    AI_INTERPRETATION_PARTIAL = "ai_interpretation_partial"


class RerunRequirement(StrEnum):
    NOT_REQUIRED = "not_required"
    RECOMMENDED = "recommended"
    REQUIRED = "required"


class RerunReason(StrEnum):
    NONE = "none"
    PROFILE_CHANGED = "profile_changed"
    ASSESSMENT_CHANGED = "assessment_changed"
    CONFIG_VERSION_CHANGED = "config_version_changed"
    AI_INTERPRETATION_INCOMPLETE = "ai_interpretation_incomplete"
    SNAPSHOT_MISSING = "snapshot_missing"


class AIInterpretationStatus(StrEnum):
    NOT_REQUESTED = "not_requested"
    PENDING = "pending"
    COMPLETE = "complete"
    PARTIAL = "partial"
    FAILED = "failed"
    FALLBACK_USED = "fallback_used"


class DiagnosisState(StrEnum):
    PROVISIONAL = "provisional"
    FINAL = "final"


class AnalysisLifecycleState(V2BaseModel):
    freshness_status: FreshnessState
    rerun_requirement: RerunRequirement = RerunRequirement.NOT_REQUIRED
    rerun_required: bool = False
    rerun_reason: RerunReason = RerunReason.NONE
    ai_interpretation_status: AIInterpretationStatus = AIInterpretationStatus.NOT_REQUESTED
    diagnosis_state: DiagnosisState = DiagnosisState.PROVISIONAL
    usable_while_stale: bool = True
    stale_explanation: str | None = Field(default=None, max_length=280)

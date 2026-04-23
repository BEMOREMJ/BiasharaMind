from __future__ import annotations

from dataclasses import dataclass
from statistics import mean
from typing import Any

from app.v2.config import SCALE_LIBRARY
from app.v2.schemas.explainability import (
    AppliedCap,
    ConfidenceLimitation,
    EvidenceGap,
    ExplainabilitySnapshot,
    ScoreDriver,
)
from app.v2.schemas.lifecycle import (
    AIInterpretationStatus,
    AnalysisLifecycleState,
    DiagnosisState,
    FreshnessState,
    RerunReason,
    RerunRequirement,
)
from app.v2.schemas.scoring import (
    AnalysisScoreSummary,
    BucketScore,
    CompletenessSummary,
    ConfidenceLabel,
    CoverageLabel,
    EvidenceConfidenceSummary,
    HealthStatus,
    SectionScore,
    StatusCapResult,
)

SECTION_WEIGHTS = {
    "market_offer_strength": 12,
    "revenue_engine": 14,
    "customer_retention_service_quality": 10,
    "financial_control_cash_discipline": 24,
    "operations_delivery_reliability": 18,
    "management_control_planning_discipline": 14,
    "team_capacity_continuity": 8,
}

KEY_SECTION_IDS = {
    "financial_control_cash_discipline",
    "operations_delivery_reliability",
    "revenue_engine",
    "management_control_planning_discipline",
}

BUCKET_WEIGHTS = {"outcome": 0.45, "control": 0.35, "risk": 0.20}

STATUS_ORDER = [
    HealthStatus.CRITICAL,
    HealthStatus.FRAGILE,
    HealthStatus.VULNERABLE,
    HealthStatus.STABLE_BUT_CONSTRAINED,
    HealthStatus.STRONG_AND_CONTROLLED,
]


@dataclass
class ScoreContext:
    answers: list[Any]
    question_map: dict[str, Any]
    section_titles: dict[str, str]
    module_parent_map: dict[str, str]
    section_question_ids: dict[str, list[str]]


def build_scale_map() -> dict[str, Any]:
    return {scale.key: scale for scale in SCALE_LIBRARY}


def _scale_for_question(question: Any, scale_map: dict[str, Any]) -> Any | None:
    return scale_map.get(getattr(question, "scale_key", None))


def score_question(answer: Any, question: Any, scale_map: dict[str, Any]) -> float | None:
    if not getattr(question, "scored", False) or not answer.is_sufficient_answer or answer.response_kind != "answered":
        return None
    scale = _scale_for_question(question, scale_map)
    if scale is None:
        return None
    if question.question_type == "select":
        options = {option.value: option.numeric_value for option in scale.options}
        if not isinstance(answer.value, str):
            return None
        return float(options[answer.value])
    if question.question_type == "number":
        if not isinstance(answer.value, (int, float)):
            return None
        span = max((scale.max_value or 0) - (scale.min_value or 0), 1)
        normalized = (float(answer.value) - (scale.min_value or 0)) / span
        return round(max(0.0, min(normalized, 1.0)) * 100, 2)
    if question.question_type == "multiselect":
        if not isinstance(answer.value, list) or not answer.value:
            return None
        options = {option.value: option.numeric_value for option in scale.options}
        return round(mean(options[item] for item in answer.value), 2)
    return None


def label_for_coverage(score: float) -> CoverageLabel:
    if score >= 85:
        return CoverageLabel.HIGH
    if score >= 65:
        return CoverageLabel.GOOD
    if score >= 40:
        return CoverageLabel.PARTIAL
    return CoverageLabel.LOW


def label_for_confidence(score: float) -> ConfidenceLabel:
    if score >= 75:
        return ConfidenceLabel.HIGH
    if score >= 55:
        return ConfidenceLabel.MODERATE
    return ConfidenceLabel.LOW


def health_status_for_score(score: float) -> HealthStatus:
    if score >= 80:
        return HealthStatus.STRONG_AND_CONTROLLED
    if score >= 65:
        return HealthStatus.STABLE_BUT_CONSTRAINED
    if score >= 50:
        return HealthStatus.VULNERABLE
    if score >= 35:
        return HealthStatus.FRAGILE
    return HealthStatus.CRITICAL


def _status_rank(status: HealthStatus) -> int:
    return STATUS_ORDER.index(status)


def _cap_status(current: HealthStatus, cap: HealthStatus) -> HealthStatus:
    return cap if _status_rank(current) > _status_rank(cap) else current


def compute_bucket_score(values: dict[str, list[float]]) -> tuple[float, list[BucketScore]]:
    present = {bucket: scores for bucket, scores in values.items() if scores}
    if not present:
        return 0.0, [BucketScore(bucket=bucket, score=0, contributing_question_count=0) for bucket in BUCKET_WEIGHTS]
    total_weight = sum(BUCKET_WEIGHTS[bucket] for bucket in present)
    final = 0.0
    bucket_scores: list[BucketScore] = []
    for bucket, weight in BUCKET_WEIGHTS.items():
        scores = values.get(bucket, [])
        bucket_average = round(mean(scores), 2) if scores else 0.0
        if scores:
            final += bucket_average * (weight / total_weight)
        bucket_scores.append(BucketScore(bucket=bucket, score=bucket_average, contributing_question_count=len(scores)))
    return round(final, 2), bucket_scores


def compute_completeness(context: ScoreContext) -> tuple[CompletenessSummary, dict[str, float]]:
    questions = list(context.question_map.values())
    answers = {answer.question_id: answer for answer in context.answers}
    essential_applicable = len([question for question in questions if question.essential])
    essential_answered = len([
        question for question in questions
        if question.essential and answers.get(question.question_id) and answers[question.question_id].is_sufficient_answer
    ])
    optional_applicable = len([question for question in questions if not question.essential])
    optional_answered = len([
        question for question in questions
        if not question.essential and answers.get(question.question_id) and answers[question.question_id].is_sufficient_answer
    ])
    essential_ratio = essential_answered / essential_applicable if essential_applicable else 1.0
    optional_ratio = optional_answered / optional_applicable if optional_applicable else 1.0
    overall = round((0.8 * essential_ratio + 0.2 * optional_ratio) * 100, 2)
    per_section = {}
    for section_id, question_ids in context.section_question_ids.items():
        section_questions = [context.question_map[question_id] for question_id in question_ids]
        section_essential = [question for question in section_questions if question.essential]
        section_optional = [question for question in section_questions if not question.essential]
        section_essential_answered = len([
            question for question in section_essential
            if answers.get(question.question_id) and answers[question.question_id].is_sufficient_answer
        ])
        section_optional_answered = len([
            question for question in section_optional
            if answers.get(question.question_id) and answers[question.question_id].is_sufficient_answer
        ])
        essential_ratio_section = section_essential_answered / len(section_essential) if section_essential else 1.0
        optional_ratio_section = section_optional_answered / len(section_optional) if section_optional else 1.0
        per_section[section_id] = round((0.8 * essential_ratio_section + 0.2 * optional_ratio_section) * 100, 2)
    return (
        CompletenessSummary(
            overall=overall,
            label=label_for_coverage(overall),
            essential_answered_sufficiently=essential_answered,
            essential_applicable=essential_applicable,
            optional_answered_sufficiently=optional_answered,
            optional_applicable=optional_applicable,
        ),
        per_section,
    )


def compute_evidence_confidence(context: ScoreContext, section_completeness: dict[str, float]) -> EvidenceConfidenceSummary:
    sufficient = [answer for answer in context.answers if answer.is_sufficient_answer]
    structured_numeric = [answer for answer in sufficient if context.question_map[answer.question_id].question_type in {"select", "number", "multiselect"}]
    numeric = [answer for answer in sufficient if context.question_map[answer.question_id].question_type == "number"]
    specificity = round((len(structured_numeric) / max(len(sufficient), 1)) * 100, 2)
    quantification = round((len(numeric) / max(len(structured_numeric), 1)) * 100, 2)
    contradictions = 0
    answers_by_id = {answer.question_id: answer for answer in context.answers}
    if (
        answers_by_id.get("risk_cash_pressure_check")
        and answers_by_id["risk_cash_pressure_check"].value == "yes"
        and answers_by_id.get("finance_cash_position_clarity")
        and isinstance(answers_by_id["finance_cash_position_clarity"].value, (int, float))
        and float(answers_by_id["finance_cash_position_clarity"].value) >= 8
    ):
        contradictions += 1
    if (
        answers_by_id.get("team_single_point_dependency")
        and answers_by_id["team_single_point_dependency"].value == "yes"
        and answers_by_id.get("team_role_coverage")
        and answers_by_id["team_role_coverage"].value == "well_managed"
    ):
        contradictions += 1
    internal_consistency = max(0.0, 100.0 - contradictions * 30.0)
    corroboration = round((len([score for score in section_completeness.values() if score >= 50]) / max(len(section_completeness), 1)) * 100, 2)
    overall = round(0.30 * specificity + 0.25 * quantification + 0.25 * internal_consistency + 0.20 * corroboration, 2)
    limitations = []
    if quantification < 40:
        limitations.append("Limited quantified evidence across the assessment.")
    if internal_consistency < 70:
        limitations.append("Some answers appear internally inconsistent.")
    if corroboration < 50:
        limitations.append("Too few sections have corroborating structured evidence.")
    if specificity < 50:
        limitations.append("Too much of the assessment relies on non-specific or missing detail.")
    return EvidenceConfidenceSummary(
        score=overall,
        label=label_for_confidence(overall),
        specificity=specificity,
        quantification=quantification,
        internal_consistency=internal_consistency,
        corroboration=corroboration,
        key_limitations=limitations,
    )


def compute_section_scores(context: ScoreContext, section_completeness: dict[str, float]) -> list[SectionScore]:
    answers_by_section: dict[str, list[Any]] = {}
    for answer in context.answers:
        answers_by_section.setdefault(answer.section_id, []).append(answer)
    scale_map = build_scale_map()
    section_scores: list[SectionScore] = []
    for section_id, title in context.section_titles.items():
        bucket_values = {"outcome": [], "control": [], "risk": []}
        for answer in answers_by_section.get(section_id, []):
            question = context.question_map[answer.question_id]
            score = score_question(answer, question, scale_map)
            if score is not None:
                bucket_values[question.bucket].append(score)
        base_score, bucket_scores = compute_bucket_score(bucket_values)
        module_scores = []
        for module_id, parent_section in context.module_parent_map.items():
            if parent_section != section_id:
                continue
            module_bucket_values = {"outcome": [], "control": [], "risk": []}
            for answer in answers_by_section.get(module_id, []):
                question = context.question_map[answer.question_id]
                score = score_question(answer, question, scale_map)
                if score is not None:
                    module_bucket_values[question.bucket].append(score)
            module_score, _ = compute_bucket_score(module_bucket_values)
            if module_score > 0:
                module_scores.append(module_score)
        module_contribution_score = round(mean(module_scores), 2) if module_scores else None
        final_score = round(base_score * 0.7 + module_contribution_score * 0.3, 2) if module_contribution_score is not None else base_score
        section_scores.append(
            SectionScore(
                section_id=section_id,
                title=title,
                score=final_score,
                bucket_scores=bucket_scores,
                completeness=section_completeness.get(section_id, 0.0),
                completeness_label=label_for_coverage(section_completeness.get(section_id, 0.0)),
                evidence_confidence=0,
                module_contribution_score=module_contribution_score,
                module_contribution_weight=0.3 if module_contribution_score is not None else None,
            )
        )
    return section_scores


def compute_overall_score(section_scores: list[SectionScore]) -> float:
    applicable = [section for section in section_scores if section.section_id in SECTION_WEIGHTS]
    numerator = sum(section.score * SECTION_WEIGHTS[section.section_id] for section in applicable)
    denominator = sum(SECTION_WEIGHTS[section.section_id] for section in applicable)
    return round(numerator / max(denominator, 1), 2)


def count_active_critical_risks(answers: list[Any]) -> int:
    critical_ids = {"risk_cash_pressure_check", "risk_compliance_exposure_check"}
    return len([answer for answer in answers if answer.question_id in critical_ids and answer.value == "yes"])


def apply_status_caps(
    overall_score: float,
    section_scores: list[SectionScore],
    active_critical_risk_count: int,
) -> tuple[HealthStatus, list[StatusCapResult], bool, str | None]:
    status = health_status_for_score(overall_score)
    caps: list[StatusCapResult] = []
    section_map = {section.section_id: section for section in section_scores}
    if section_map.get("financial_control_cash_discipline") and section_map["financial_control_cash_discipline"].score < 35:
        status = _cap_status(status, HealthStatus.VULNERABLE)
        caps.append(StatusCapResult(code="financial_control_cap", label="Financial Control cap", capped_status=HealthStatus.VULNERABLE, reason="Financial Control score below 35 cannot exceed Vulnerable."))
    if section_map.get("operations_delivery_reliability") and section_map["operations_delivery_reliability"].score < 35:
        status = _cap_status(status, HealthStatus.VULNERABLE)
        caps.append(StatusCapResult(code="operations_cap", label="Operations cap", capped_status=HealthStatus.VULNERABLE, reason="Operations score below 35 cannot exceed Vulnerable."))
    if active_critical_risk_count >= 2:
        status = _cap_status(status, HealthStatus.FRAGILE)
        caps.append(StatusCapResult(code="critical_risk_cap", label="Critical risk cap", capped_status=HealthStatus.FRAGILE, reason="Two or more active critical risks cannot exceed Fragile."))
    low_key_sections = [section for section in section_scores if section.section_id in KEY_SECTION_IDS and section.completeness < 50]
    provisional = len(low_key_sections) > 0
    provisional_reason = "Essential coverage is too low in key sections, so the diagnosis remains provisional." if provisional else None
    return status, caps, provisional, provisional_reason


def build_explainability(
    section_scores: list[SectionScore],
    evidence_confidence: EvidenceConfidenceSummary,
    caps: list[StatusCapResult],
    provisional_reason: str | None,
) -> ExplainabilitySnapshot:
    return ExplainabilitySnapshot(
        score_drivers=[
            ScoreDriver(
                code=f"section_{section.section_id}",
                label=section.title,
                direction="mixed",
                detail=f"{section.title} scored {section.score:.1f} with {section.completeness_label.value.replace('_', ' ')}.",
                evidence_refs=[section.section_id],
            )
            for section in section_scores
        ],
        caps_applied=[
            AppliedCap(code=cap.code, label=cap.label, reason=cap.reason, capped_to=None)
            for cap in caps
        ],
        missing_or_weak_evidence=[
            EvidenceGap(area="assessment_coverage", detail=limitation, severity="medium")
            for limitation in evidence_confidence.key_limitations[:5]
        ],
        confidence_limitations=[
            ConfidenceLimitation(code=f"confidence_{index}", detail=limitation, impact="Lowers certainty in the deterministic evidence-confidence layer.")
            for index, limitation in enumerate(evidence_confidence.key_limitations)
        ] + (
            [ConfidenceLimitation(code="provisional_status", detail=provisional_reason, impact="The current status should be treated as provisional until key essential answers improve.")]
            if provisional_reason else []
        ),
    )


def build_lifecycle(provisional: bool, provisional_reason: str | None) -> AnalysisLifecycleState:
    return AnalysisLifecycleState(
        freshness_status=FreshnessState.PROVISIONAL if provisional else FreshnessState.FRESH,
        rerun_requirement=RerunRequirement.NOT_REQUIRED,
        rerun_required=False,
        rerun_reason=RerunReason.NONE,
        ai_interpretation_status=AIInterpretationStatus.NOT_REQUESTED,
        diagnosis_state=DiagnosisState.PROVISIONAL if provisional else DiagnosisState.FINAL,
        usable_while_stale=True,
        stale_explanation=provisional_reason,
    )


def run_deterministic_scoring(context: ScoreContext) -> tuple[AnalysisScoreSummary, ExplainabilitySnapshot, AnalysisLifecycleState]:
    completeness, section_completeness = compute_completeness(context)
    section_scores = compute_section_scores(context, section_completeness)
    evidence_confidence = compute_evidence_confidence(context, section_completeness)
    for section in section_scores:
        section.evidence_confidence = evidence_confidence.score
    overall = compute_overall_score(section_scores)
    active_critical_risk_count = count_active_critical_risks(context.answers)
    status, caps, provisional, provisional_reason = apply_status_caps(overall, section_scores, active_critical_risk_count)
    summary = AnalysisScoreSummary(
        overall_health_score=overall,
        overall_status=status,
        section_scores=section_scores,
        completeness=completeness,
        evidence_confidence=evidence_confidence,
        active_critical_risk_count=active_critical_risk_count,
        caps_applied=caps,
    )
    return summary, build_explainability(section_scores, evidence_confidence, caps, provisional_reason), build_lifecycle(provisional, provisional_reason)

from __future__ import annotations

from dataclasses import dataclass
from statistics import mean
from typing import Any

from app.v2.config import ACTION_FAMILY_REGISTRY, CRITICAL_RISK_TAXONOMY, ISSUE_TAXONOMY
from app.v2.schemas.diagnosis import (
    CriticalRiskRead,
    DiagnosisSummaryRead,
    IssueCandidateRead,
    PriorityRead,
    RoadmapInputItemRead,
    RoadmapInputPackageRead,
    WatchlistItemRead,
)
from app.v2.schemas.explainability import PriorityRationale, WatchlistRationale
from app.v2.schemas.scoring import AnalysisScoreSummary, SectionScore

SECTION_DIMENSIONS = {
    "market_offer_strength": "market",
    "revenue_engine": "revenue",
    "customer_retention_service_quality": "customer",
    "financial_control_cash_discipline": "finance",
    "operations_delivery_reliability": "operations",
    "management_control_planning_discipline": "management",
    "team_capacity_continuity": "team",
}

QUESTION_TO_SECTION = {
    "market_offer_clarity": "market_offer_strength",
    "revenue_sales_pipeline_repeatability": "revenue_engine",
    "revenue_target_confidence": "revenue_engine",
    "customer_follow_up_consistency": "customer_retention_service_quality",
    "customer_service_issue_visibility": "customer_retention_service_quality",
    "finance_reporting_rhythm": "financial_control_cash_discipline",
    "finance_cash_position_clarity": "financial_control_cash_discipline",
    "collections_follow_up_visibility": "financial_control_cash_discipline",
    "operations_process_stability": "operations_delivery_reliability",
    "operations_issue_visibility": "operations_delivery_reliability",
    "inventory_accuracy_visibility": "operations_delivery_reliability",
    "service_capacity_planning": "operations_delivery_reliability",
    "production_flow_stability": "operations_delivery_reliability",
    "management_priority_clarity": "management_control_planning_discipline",
    "management_decision_data_quality": "management_control_planning_discipline",
    "team_role_coverage": "team_capacity_continuity",
    "team_single_point_dependency": "team_capacity_continuity",
}

TEXT_QUESTION_HINTS = {
    "financial_control_cash_discipline": ["finance_surprise_notes", "collections_delay_notes"],
    "operations_delivery_reliability": ["operations_reliability_notes", "inventory_stock_issue_notes", "service_scheduling_breakdown_notes", "production_failure_notes"],
    "customer_retention_service_quality": ["customer_quality_notes"],
    "revenue_engine": ["revenue_constraint_notes"],
    "management_control_planning_discipline": ["management_control_notes"],
    "team_capacity_continuity": ["team_capacity_notes"],
    "market_offer_strength": ["market_offer_shift_notes"],
}

ISSUE_RULES = {
    "FINANCE_VISIBILITY_GAP": {
        "section_id": "financial_control_cash_discipline",
        "questions": ["finance_reporting_rhythm", "finance_cash_position_clarity"],
        "bucket": "control",
        "dependencies": ["A basic weekly cash review rhythm"],
        "success_metrics": ["Weekly cash position updated on time", "No surprise cash gaps without an early warning"],
        "visibility_issue": True,
        "stabilization": True,
    },
    "REACTIVE_CASH_MANAGEMENT": {
        "section_id": "financial_control_cash_discipline",
        "questions": ["risk_cash_pressure_check", "finance_cash_position_clarity"],
        "bucket": "outcome",
        "risk_codes": ["CRITICAL_CASH_PRESSURE"],
        "dependencies": ["A visible short-term cash view", "Owner review of due obligations and inflows"],
        "success_metrics": ["Near-term cash forecast updated weekly", "Cash pressure events are reduced"],
        "stabilization": True,
    },
    "OVERDUE_RECEIVABLES_TRAP": {
        "section_id": "financial_control_cash_discipline",
        "questions": ["collections_follow_up_visibility"],
        "bucket": "control",
        "risk_codes": ["CRITICAL_COLLECTIONS_STRAIN"],
        "dependencies": ["Overdue list with named owners", "Simple follow-up cadence"],
        "success_metrics": ["Overdue balances reviewed weekly", "Average days overdue start falling"],
        "stabilization": True,
    },
    "DELIVERY_UNRELIABILITY": {
        "section_id": "operations_delivery_reliability",
        "questions": ["operations_process_stability", "operations_issue_visibility", "inventory_accuracy_visibility", "service_capacity_planning", "production_flow_stability"],
        "bucket": "outcome",
        "dependencies": ["A clear owner for daily operating exceptions"],
        "success_metrics": ["Missed commitments decline", "Operating issues are logged within one day"],
        "stabilization": True,
    },
    "OPERATIONS_VISIBILITY_GAP": {
        "section_id": "operations_delivery_reliability",
        "questions": ["operations_issue_visibility", "inventory_accuracy_visibility"],
        "bucket": "control",
        "dependencies": ["A short weekly review rhythm", "A small set of operating numbers"],
        "success_metrics": ["Key operating delays are visible weekly", "Stock or schedule issues are detected earlier"],
        "visibility_issue": True,
        "stabilization": True,
    },
    "HIGH_COMPLAINT_SERVICE_BREAKDOWN": {
        "section_id": "customer_retention_service_quality",
        "questions": ["customer_follow_up_consistency", "customer_service_issue_visibility"],
        "bucket": "outcome",
        "dependencies": ["A basic complaint and follow-up loop"],
        "success_metrics": ["Follow-up completion rate improves", "Repeat complaints decline"],
        "stabilization": True,
    },
    "SALES_PIPELINE_WEAKNESS": {
        "section_id": "revenue_engine",
        "questions": ["revenue_sales_pipeline_repeatability", "revenue_target_confidence"],
        "bucket": "outcome",
        "dependencies": ["A visible lead and follow-up list"],
        "success_metrics": ["Pipeline follow-up completion improves", "Revenue confidence becomes more predictable"],
        "growth": True,
        "visibility_issue": True,
    },
    "MANAGEMENT_VISIBILITY_GAP": {
        "section_id": "management_control_planning_discipline",
        "questions": ["management_priority_clarity", "management_decision_data_quality"],
        "bucket": "control",
        "dependencies": ["A simple weekly management review", "Named owners for core priorities"],
        "success_metrics": ["Priority review happens weekly", "Decision inputs are visible before review meetings"],
        "visibility_issue": True,
        "stabilization": True,
    },
    "TEAM_CONTINUITY_RISK": {
        "section_id": "team_capacity_continuity",
        "questions": ["team_role_coverage", "team_single_point_dependency"],
        "bucket": "risk",
        "risk_codes": ["CRITICAL_OWNER_DEPENDENCY"],
        "dependencies": ["Coverage for critical recurring tasks"],
        "success_metrics": ["Single-point approvals are reduced", "Critical work can continue during absence"],
        "stabilization": True,
    },
    "MARKET_OFFER_GAP": {
        "section_id": "market_offer_strength",
        "questions": ["market_offer_clarity"],
        "bucket": "outcome",
        "dependencies": ["A clearer description of the main offer"],
        "success_metrics": ["Offer message becomes consistent across channels"],
        "growth": True,
    },
    "GROWTH_BLOCKER_UNRESOLVED": {
        "section_id": "revenue_engine",
        "questions": ["revenue_target_confidence"],
        "bucket": "outcome",
        "dependencies": ["Clarity on the single growth constraint"],
        "success_metrics": ["The named growth constraint is reduced or removed"],
        "growth": True,
    },
}


@dataclass
class DiagnosisContext:
    profile: Any
    summary: AnalysisScoreSummary
    answers: list[Any]
    question_map: dict[str, Any]
    section_titles: dict[str, str]
    explainability: Any


def _taxonomy_map(entries: list[Any]) -> dict[str, Any]:
    return {entry.code: entry for entry in entries}


ISSUE_MAP = _taxonomy_map(ISSUE_TAXONOMY)
RISK_MAP = _taxonomy_map(CRITICAL_RISK_TAXONOMY)
ACTION_MAP = _taxonomy_map(ACTION_FAMILY_REGISTRY)


def _clamp(value: float, minimum: float = 0.0, maximum: float = 100.0) -> float:
    return round(max(minimum, min(value, maximum)), 2)


def _answer_map(context: DiagnosisContext) -> dict[str, Any]:
    return {answer.question_id: answer for answer in context.answers}


def _section_map(summary: AnalysisScoreSummary) -> dict[str, SectionScore]:
    return {section.section_id: section for section in summary.section_scores}


def _bucket_score(section: SectionScore, bucket: str) -> float:
    for item in section.bucket_scores:
        if item.bucket == bucket:
            return item.score
    return 0.0


def _question_score(answer: Any, question: Any) -> float | None:
    if answer is None or not answer.is_sufficient_answer or answer.response_kind != "answered":
        return None
    if question.question_type == "number" and isinstance(answer.value, (int, float)):
        return _clamp(float(answer.value) * 10)
    if isinstance(answer.value, str):
        scale_key = getattr(question, "scale_key", None)
        if scale_key == "maturity_4":
            return {"not_in_place": 25, "ad_hoc": 45, "partly_defined": 65, "well_managed": 85}.get(answer.value)
        if scale_key == "coverage_4":
            return {"not_visible": 20, "basic_visibility": 45, "usable_visibility": 65, "strong_visibility": 85}.get(answer.value)
        if scale_key == "frequency_4":
            return {"rarely": 25, "sometimes": 50, "weekly": 72, "consistently": 85}.get(answer.value)
        if scale_key == "yes_no":
            return {"yes": 85, "no": 25}.get(answer.value)
    return None


def materialize_critical_risks(context: DiagnosisContext) -> list[CriticalRiskRead]:
    answers = _answer_map(context)
    risks: list[CriticalRiskRead] = []

    if answers.get("risk_cash_pressure_check") and answers["risk_cash_pressure_check"].value == "yes":
        taxonomy = RISK_MAP["CRITICAL_CASH_PRESSURE"]
        risks.append(
            CriticalRiskRead(
                code=taxonomy.code,
                title=taxonomy.label,
                severity=taxonomy.severity,
                evidence_question_ids=["risk_cash_pressure_check", "finance_cash_position_clarity"],
                evidence_summary="Recent cash pressure was flagged directly in the risk checks.",
                recommended_action_families=taxonomy.action_family_codes,
            )
        )

    if answers.get("team_single_point_dependency") and answers["team_single_point_dependency"].value == "yes":
        taxonomy = RISK_MAP["CRITICAL_OWNER_DEPENDENCY"]
        risks.append(
            CriticalRiskRead(
                code=taxonomy.code,
                title=taxonomy.label,
                severity=taxonomy.severity,
                evidence_question_ids=["team_single_point_dependency", "team_role_coverage"],
                evidence_summary="The assessment indicates a high dependency on one person for critical continuity.",
                recommended_action_families=taxonomy.action_family_codes,
            )
        )

    if answers.get("risk_compliance_exposure_check") and answers["risk_compliance_exposure_check"].value == "yes":
        taxonomy = RISK_MAP["CRITICAL_COMPLIANCE_EXPOSURE"]
        risks.append(
            CriticalRiskRead(
                code=taxonomy.code,
                title=taxonomy.label,
                severity=taxonomy.severity,
                evidence_question_ids=["risk_compliance_exposure_check"],
                evidence_summary="Compliance exposure was flagged as a material risk in the critical-risk checks.",
                recommended_action_families=taxonomy.action_family_codes,
            )
        )

    if (
        answers.get("collections_follow_up_visibility")
        and answers["collections_follow_up_visibility"].value in {"not_visible", "basic_visibility"}
        and getattr(context.profile, "credit_sales_exposure", None) in {"moderate", "high"}
    ):
        taxonomy = RISK_MAP["CRITICAL_COLLECTIONS_STRAIN"]
        risks.append(
            CriticalRiskRead(
                code=taxonomy.code,
                title=taxonomy.label,
                severity=taxonomy.severity,
                evidence_question_ids=["collections_follow_up_visibility"],
                evidence_summary="Collections visibility is weak while credit exposure is materially present.",
                recommended_action_families=taxonomy.action_family_codes,
            )
        )

    return risks


def _contradiction_signals(context: DiagnosisContext) -> dict[str, list[str]]:
    answers = _answer_map(context)
    signals: dict[str, list[str]] = {}
    if (
        answers.get("risk_cash_pressure_check")
        and answers["risk_cash_pressure_check"].value == "yes"
        and answers.get("finance_cash_position_clarity")
        and isinstance(answers["finance_cash_position_clarity"].value, (int, float))
        and float(answers["finance_cash_position_clarity"].value) >= 8
    ):
        signals.setdefault("FINANCE_VISIBILITY_GAP", []).append("risk_cash_pressure_check")
    if (
        answers.get("team_single_point_dependency")
        and answers["team_single_point_dependency"].value == "yes"
        and answers.get("team_role_coverage")
        and answers["team_role_coverage"].value == "well_managed"
    ):
        signals.setdefault("TEAM_CONTINUITY_RISK", []).append("team_single_point_dependency")
    return signals


def _goal_fit_adjustment(goal: str, issue_code: str, dimension: str) -> float:
    strong_fit = {
        "grow_sales": {"SALES_PIPELINE_WEAKNESS", "MARKET_OFFER_GAP", "GROWTH_BLOCKER_UNRESOLVED"},
        "improve_cash_flow": {"FINANCE_VISIBILITY_GAP", "REACTIVE_CASH_MANAGEMENT", "OVERDUE_RECEIVABLES_TRAP"},
        "improve_efficiency": {"DELIVERY_UNRELIABILITY", "OPERATIONS_VISIBILITY_GAP", "MANAGEMENT_VISIBILITY_GAP", "TEAM_CONTINUITY_RISK"},
        "stabilize_operations": {"REACTIVE_CASH_MANAGEMENT", "DELIVERY_UNRELIABILITY", "HIGH_COMPLAINT_SERVICE_BREAKDOWN", "TEAM_CONTINUITY_RISK", "MANAGEMENT_VISIBILITY_GAP"},
        "increase_customer_retention": {"HIGH_COMPLAINT_SERVICE_BREAKDOWN", "SALES_PIPELINE_WEAKNESS"},
        "prepare_to_expand": {"MANAGEMENT_VISIBILITY_GAP", "FINANCE_VISIBILITY_GAP", "DELIVERY_UNRELIABILITY"},
    }
    weak_fit_dimensions = {
        "grow_sales": {"finance"},
        "improve_cash_flow": {"market"},
        "improve_efficiency": {"market"},
    }
    if issue_code in strong_fit.get(goal, set()):
        return 1.1
    if dimension in weak_fit_dimensions.get(goal, set()):
        return 0.9
    return 1.0


def _feasibility_score(context: DiagnosisContext, action_family_code: str) -> float:
    action_family = ACTION_MAP[action_family_code]
    score = {"now": 72.0, "next": 60.0, "later": 45.0}[action_family.default_horizon]
    capacity = getattr(context.profile, "improvement_capacity", None)
    if capacity is not None:
        score += {"very_limited": -20, "limited": -10, "moderate": 0, "strong": 8}.get(capacity.time_capacity, 0)
        score += {"none": -15, "tight": -8, "moderate": 0, "flexible": 6}.get(capacity.budget_flexibility, 0)
        score += {"not_open": -10, "cautiously_open": -4, "open": 5}.get(capacity.tool_hire_openness, 0)
    if getattr(context.profile, "record_availability", None) == "minimal" and action_family_code in {"METRIC_VISIBILITY", "FINANCIAL_CONTROL"}:
        score -= 8
    return _clamp(score)


def _leverage_score(issue_code: str, dimension: str, visibility_issue: bool, stabilization: bool) -> float:
    score = 58.0
    if visibility_issue:
        score += 14
    if stabilization:
        score += 10
    if dimension in {"finance", "operations", "management"}:
        score += 6
    if issue_code == "GROWTH_BLOCKER_UNRESOLVED":
        score += 8
    return _clamp(score)


def _impact_score(section: SectionScore, dimension: str, has_critical_risk: bool) -> float:
    section_weight = {
        "market_offer_strength": 12,
        "revenue_engine": 14,
        "customer_retention_service_quality": 10,
        "financial_control_cash_discipline": 24,
        "operations_delivery_reliability": 18,
        "management_control_planning_discipline": 14,
        "team_capacity_continuity": 8,
    }.get(section.section_id, 8)
    base = 45 + (section_weight / 24) * 25 + max(0, (50 - section.score) * 0.35)
    if has_critical_risk:
        base += 12
    if dimension in {"finance", "operations"}:
        base += 6
    return _clamp(base)


def _confidence_score(context: DiagnosisContext, trigger_count: int, has_critical_risk: bool, direct_low: bool, has_text: bool) -> float:
    score = context.summary.evidence_confidence.score * 0.8
    score += trigger_count * 8
    if direct_low:
        score += 10
    if has_text:
        score += 5
    if has_critical_risk:
        score += 12
    return _clamp(score)


def _priority_score(issue: IssueCandidateRead) -> tuple[float, float]:
    priority = (
        0.25 * issue.severity_score
        + 0.25 * issue.impact_score
        + 0.20 * issue.urgency_score
        + 0.15 * issue.feasibility_score
        + 0.10 * issue.leverage_score
        + 0.05 * issue.confidence_score
    )
    return round(priority, 2), round(priority * issue.goal_fit_adjustment, 2)


def generate_issue_candidates(context: DiagnosisContext, critical_risks: list[CriticalRiskRead]) -> list[IssueCandidateRead]:
    section_map = _section_map(context.summary)
    answers = _answer_map(context)
    contradiction_map = _contradiction_signals(context)
    active_risk_codes = {risk.code for risk in critical_risks}
    issues: list[IssueCandidateRead] = []

    for issue_code, rule in ISSUE_RULES.items():
        taxonomy = ISSUE_MAP[issue_code]
        section = section_map.get(rule["section_id"])
        if section is None:
            continue
        question_ids = [question_id for question_id in rule["questions"] if question_id in answers]
        direct_scores = []
        for question_id in question_ids:
            question = context.question_map.get(question_id)
            answer = answers.get(question_id)
            if question is not None and answer is not None:
                score = _question_score(answer, question)
                if score is not None:
                    direct_scores.append((question_id, score))
        direct_low_ids = [question_id for question_id, score in direct_scores if score <= 25]
        bucket_score = _bucket_score(section, rule["bucket"])
        bucket_trigger = bucket_score < 50
        text_ids = [
            question_id
            for question_id in TEXT_QUESTION_HINTS.get(rule["section_id"], [])
            if answers.get(question_id) and isinstance(answers[question_id].value, str) and answers[question_id].value.strip()
        ]
        contradiction_ids = contradiction_map.get(issue_code, [])
        linked_risk_codes = [code for code in rule.get("risk_codes", []) if code in active_risk_codes]
        if issue_code == "FINANCE_VISIBILITY_GAP" and "CRITICAL_CASH_PRESSURE" in active_risk_codes:
            linked_risk_codes.append("CRITICAL_CASH_PRESSURE")
        if issue_code == "MANAGEMENT_VISIBILITY_GAP" and "CRITICAL_COMPLIANCE_EXPOSURE" in active_risk_codes:
            linked_risk_codes.append("CRITICAL_COMPLIANCE_EXPOSURE")
        linked_risk_codes = list(dict.fromkeys(linked_risk_codes))

        if not any([direct_low_ids, bucket_trigger, text_ids, contradiction_ids, linked_risk_codes]):
            continue

        evidence_question_ids = list(dict.fromkeys(direct_low_ids + contradiction_ids + text_ids + question_ids))
        evidence_bits = []
        if direct_low_ids:
            evidence_bits.append("one or more directly linked structured answers are at the floor")
        if bucket_trigger:
            evidence_bits.append(f"the {rule['bucket']} bucket is below 50")
        if contradiction_ids:
            evidence_bits.append("a contradiction pattern suggests hidden weakness")
        if text_ids:
            evidence_bits.append("text responses in this area add supporting context")
        if linked_risk_codes:
            evidence_bits.append("a linked critical risk is active")

        severity_base = {"low": 40, "medium": 55, "high": 75, "critical": 88}[taxonomy.severity]
        severity_score = severity_base + (12 if direct_low_ids else 0) + max(0, (50 - section.score) * 0.25) + (8 if linked_risk_codes else 0)
        urgency_score = 52 + max(0, (45 - section.score) * 0.8) + (15 if linked_risk_codes else 0) + (10 if bucket_score < 35 else 0)
        action_family = taxonomy.action_family_codes[0]
        feasibility_score = _feasibility_score(context, action_family)
        dimension = SECTION_DIMENSIONS.get(rule["section_id"], rule["section_id"])
        leverage_score = _leverage_score(issue_code, dimension, rule.get("visibility_issue", False), rule.get("stabilization", False))
        confidence_score = _confidence_score(
            context=context,
            trigger_count=len(evidence_bits),
            has_critical_risk=bool(linked_risk_codes),
            direct_low=bool(direct_low_ids),
            has_text=bool(text_ids),
        )
        impact_score = _impact_score(section, dimension, bool(linked_risk_codes))
        goal_fit_adjustment = _goal_fit_adjustment(getattr(context.profile, "primary_business_goal", ""), issue_code, dimension)

        issue = IssueCandidateRead(
            issue_code=issue_code,
            title=taxonomy.label,
            dimension=dimension,
            evidence_question_ids=evidence_question_ids,
            evidence_summary=f"{taxonomy.description} Evidence indicates that {'; '.join(evidence_bits)}.",
            severity_score=_clamp(severity_score),
            urgency_score=_clamp(urgency_score),
            impact_score=impact_score,
            feasibility_score=feasibility_score,
            leverage_score=leverage_score,
            confidence_score=confidence_score,
            critical_risk_links=linked_risk_codes,
            recommended_action_family=action_family,
            dependencies=rule["dependencies"],
            goal_fit_adjustment=goal_fit_adjustment,
            priority_score=0,
            adjusted_priority_score=0,
        )
        priority_score, adjusted_priority_score = _priority_score(issue)
        issue.priority_score = priority_score
        issue.adjusted_priority_score = adjusted_priority_score
        issues.append(issue)

    return sorted(issues, key=lambda item: item.adjusted_priority_score, reverse=True)


def _stabilization_trigger(issues: list[IssueCandidateRead], critical_risks: list[CriticalRiskRead]) -> bool:
    stabilization_codes = {
        "REACTIVE_CASH_MANAGEMENT",
        "OVERDUE_RECEIVABLES_TRAP",
        "DELIVERY_UNRELIABILITY",
        "HIGH_COMPLAINT_SERVICE_BREAKDOWN",
    }
    return any(issue.issue_code in stabilization_codes and issue.severity_score >= 70 for issue in issues) or bool(critical_risks)


def _visibility_priority_bonus(issue: IssueCandidateRead) -> float:
    return 12.0 if issue.issue_code in {"FINANCE_VISIBILITY_GAP", "OPERATIONS_VISIBILITY_GAP", "MANAGEMENT_VISIBILITY_GAP", "SALES_PIPELINE_WEAKNESS"} else 0.0


def _success_metrics_for_issue(issue_code: str) -> list[str]:
    return ISSUE_RULES[issue_code]["success_metrics"]


def rank_priorities(
    context: DiagnosisContext,
    issues: list[IssueCandidateRead],
    critical_risks: list[CriticalRiskRead],
) -> tuple[list[PriorityRead], list[WatchlistItemRead], DiagnosisSummaryRead, RoadmapInputPackageRead]:
    stabilization_first = _stabilization_trigger(issues, critical_risks)
    ranked: list[tuple[float, IssueCandidateRead, str | None]] = []
    watchlist_pool: list[WatchlistItemRead] = []

    for issue in issues:
        score = issue.adjusted_priority_score
        reason: str | None = None
        issue_rule = ISSUE_RULES.get(issue.issue_code, {})

        if issue.confidence_score < 40 and not issue.critical_risk_links:
            watchlist_pool.append(
                WatchlistItemRead(
                    issue_code=issue.issue_code,
                    title=issue.title,
                    recommended_action_family=issue.recommended_action_family,
                    adjusted_priority_score=issue.adjusted_priority_score,
                    watchlist_reason="Confidence is too low for top-priority placement without critical-risk support.",
                    critical_risk_links=issue.critical_risk_links,
                )
            )
            continue

        if issue.feasibility_score < 35 and not issue.critical_risk_links:
            watchlist_pool.append(
                WatchlistItemRead(
                    issue_code=issue.issue_code,
                    title=issue.title,
                    recommended_action_family=issue.recommended_action_family,
                    adjusted_priority_score=issue.adjusted_priority_score,
                    watchlist_reason="Feasibility is too low right now, so this issue belongs on the watchlist.",
                    critical_risk_links=issue.critical_risk_links,
                )
            )
            continue

        if stabilization_first and issue.issue_code in {"SALES_PIPELINE_WEAKNESS", "MARKET_OFFER_GAP", "GROWTH_BLOCKER_UNRESOLVED"}:
            score -= 18
            reason = "Stabilization issues must rank ahead of growth issues right now."

        if stabilization_first and issue_rule.get("stabilization"):
            score += 14
            reason = reason or "Stabilization-first sequencing is active because the business has severe control or critical-risk pressure."

        if stabilization_first and issue.critical_risk_links:
            score += 18
            reason = reason or "A linked critical risk keeps this issue ahead of lower-risk optimization work."

        if issue.issue_code in {"FINANCE_VISIBILITY_GAP", "OPERATIONS_VISIBILITY_GAP", "MANAGEMENT_VISIBILITY_GAP"}:
            score += _visibility_priority_bonus(issue)
            reason = reason or "Visibility has to improve before deeper optimization work will stick."

        ranked.append((score, issue, reason))

    ranked.sort(key=lambda item: item[0], reverse=True)

    top_priorities = [
        PriorityRead(
            issue_code=issue.issue_code,
            title=issue.title,
            recommended_action_family=issue.recommended_action_family,
            adjusted_priority_score=round(score, 2),
            why_selected=reason
            or f"This issue combines high severity, impact, and urgency with a realistic next action family in {issue.recommended_action_family}.",
            sequencing_notes=[
                "Start with the minimum control or visibility change needed to create traction."
                if issue.issue_code in {"FINANCE_VISIBILITY_GAP", "OPERATIONS_VISIBILITY_GAP", "MANAGEMENT_VISIBILITY_GAP"}
                else "Address this before lower-leverage optimization work."
            ],
            dependencies=issue.dependencies,
            critical_risk_links=issue.critical_risk_links,
            suggested_success_metrics=_success_metrics_for_issue(issue.issue_code),
        )
        for score, issue, reason in ranked[:3]
    ]

    selected_codes = {priority.issue_code for priority in top_priorities}
    for _, issue, reason in ranked[3:]:
        if len(watchlist_pool) >= 2:
            break
        watchlist_pool.append(
            WatchlistItemRead(
                issue_code=issue.issue_code,
                title=issue.title,
                recommended_action_family=issue.recommended_action_family,
                adjusted_priority_score=issue.adjusted_priority_score,
                watchlist_reason=reason or "This issue matters, but it sits behind the selected top priorities for now.",
                critical_risk_links=issue.critical_risk_links,
            )
        )

    watchlist = watchlist_pool[:2]

    strongest_sections = sorted(context.summary.section_scores, key=lambda section: section.score, reverse=True)[:2]
    weakest_sections = sorted(context.summary.section_scores, key=lambda section: section.score)[:2]
    top_constraints = [priority.title for priority in top_priorities[:3]]

    action_counts: dict[str, int] = {}
    for issue in issues:
        action_counts[issue.recommended_action_family] = action_counts.get(issue.recommended_action_family, 0) + 1
    root_cause_patterns = [
        f"{ACTION_MAP[action_family].label} is recurring across the diagnosis."
        for action_family, count in sorted(action_counts.items(), key=lambda item: item[1], reverse=True)
        if count >= 2
    ][:3]
    if critical_risks:
        root_cause_patterns.append("Critical-risk exposure is reinforcing the need for stabilization-first sequencing.")
    root_cause_patterns = root_cause_patterns[:5]

    diagnosis = DiagnosisSummaryRead(
        strongest_areas=[section.title for section in strongest_sections],
        weakest_areas=[section.title for section in weakest_sections],
        primary_bottleneck=top_priorities[0].title if top_priorities else None,
        top_constraints=top_constraints,
        root_cause_patterns=root_cause_patterns,
    )

    roadmap_items = [
        RoadmapInputItemRead(
            issue_code=priority.issue_code,
            action_family=priority.recommended_action_family,
            dependencies=priority.dependencies,
            feasibility_context=f"Current feasibility for {priority.recommended_action_family} is shaped by the business's available time, budget, and openness to simple tooling or support.",
            suggested_success_metrics=priority.suggested_success_metrics,
            sequencing_notes=priority.sequencing_notes,
        )
        for priority in top_priorities
    ]
    roadmap_inputs = RoadmapInputPackageRead(
        selected_action_families=list(dict.fromkeys(item.action_family for item in roadmap_items)),
        dependencies=list(dict.fromkeys(dep for item in roadmap_items for dep in item.dependencies)),
        feasibility_context=[item.feasibility_context for item in roadmap_items],
        suggested_success_metrics=list(dict.fromkeys(metric for item in roadmap_items for metric in item.suggested_success_metrics)),
        sequencing_notes=list(dict.fromkeys(note for item in roadmap_items for note in item.sequencing_notes)),
        items=roadmap_items,
    )
    return top_priorities, watchlist, diagnosis, roadmap_inputs


def build_priority_rationales(priorities: list[PriorityRead], critical_risks: list[CriticalRiskRead]) -> list[PriorityRationale]:
    return [
        PriorityRationale(
            priority_code=priority.issue_code,
            summary=priority.why_selected,
            contributing_issue_codes=[priority.issue_code],
            contributing_risk_codes=priority.critical_risk_links or [risk.code for risk in critical_risks[:1]],
        )
        for priority in priorities
    ]


def build_watchlist_rationales(watchlist: list[WatchlistItemRead]) -> list[WatchlistRationale]:
    return [
        WatchlistRationale(
            watchlist_code=item.issue_code,
            summary=item.watchlist_reason,
            trigger_condition="Revisit after the current top priorities have traction or more evidence improves confidence.",
        )
        for item in watchlist
    ]

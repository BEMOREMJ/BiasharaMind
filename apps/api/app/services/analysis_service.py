from datetime import UTC, datetime
from uuid import uuid4

from app.repositories.analysis_repository import analysis_repository
from app.schemas.analysis import (
    AnalysisCategoryScore,
    AnalysisSummaryRead,
    PriorityRecommendation,
)
from app.services.assessment_service import assessment_service

SECTION_LABELS = {
    "operations": "Operations",
    "sales_marketing": "Sales and Marketing",
    "customer_management": "Customer Management",
    "finance_reporting": "Finance and Reporting",
    "team_workflows": "Team Workflows",
    "digital_tools": "Digital Tools",
    "growth_blockers": "Growth Blockers",
}

SELECT_SCORES = {
    "operations_process_documented": {
        "not_documented": 25,
        "owner_memory": 40,
        "partly_documented": 65,
        "well_documented": 85,
    },
    "sales_new_customers_channel": {
        "walk_in": 55,
        "referrals": 70,
        "social_media": 68,
        "paid_ads": 72,
        "outreach": 64,
    },
    "customer_follow_up_frequency": {
        "rarely": 30,
        "reactive": 45,
        "sometimes": 65,
        "consistently": 85,
    },
    "finance_reporting_frequency": {
        "rarely": 25,
        "monthly": 55,
        "weekly": 75,
        "daily": 88,
    },
    "team_role_clarity": {
        "very_unclear": 25,
        "somewhat_unclear": 45,
        "mostly_clear": 72,
        "very_clear": 88,
    },
    "tools_primary_stack": {
        "mostly_manual": 25,
        "disconnected_tools": 48,
        "partial_system": 68,
        "organized_stack": 86,
    },
    "growth_blocker_urgency": {
        "low": 85,
        "moderate": 65,
        "high": 40,
        "critical": 25,
    },
}

PRIORITY_RULES = {
    "operations": {
        "title": "Standardize core operations",
        "why": "Document repeatable operating routines so daily execution is less dependent on memory.",
        "effort": "medium",
        "cost_band": "low",
        "expected_impact": "high",
    },
    "sales_marketing": {
        "title": "Strengthen sales predictability",
        "why": "Improve acquisition and confidence in monthly targets with a more repeatable sales motion.",
        "effort": "medium",
        "cost_band": "medium",
        "expected_impact": "high",
    },
    "customer_management": {
        "title": "Build a repeat-customer follow-up routine",
        "why": "A consistent customer rhythm helps retention and surfaces better feedback sooner.",
        "effort": "low",
        "cost_band": "low",
        "expected_impact": "high",
    },
    "finance_reporting": {
        "title": "Improve financial visibility",
        "why": "Faster reporting and cash visibility reduce operational surprises and improve decisions.",
        "effort": "medium",
        "cost_band": "low",
        "expected_impact": "high",
    },
    "team_workflows": {
        "title": "Clarify team ownership",
        "why": "Clear roles and accountability reduce dropped tasks and execution bottlenecks.",
        "effort": "medium",
        "cost_band": "low",
        "expected_impact": "medium",
    },
    "digital_tools": {
        "title": "Reduce manual work with better tools",
        "why": "Improving the tool stack can remove repetitive manual effort and increase operational trust.",
        "effort": "medium",
        "cost_band": "medium",
        "expected_impact": "high",
    },
    "growth_blockers": {
        "title": "Address the main growth blocker",
        "why": "Focusing on the most urgent blocker creates the clearest path to near-term business momentum.",
        "effort": "high",
        "cost_band": "medium",
        "expected_impact": "high",
    },
}


def score_text_response(value: str) -> float:
    length = len(value.strip())
    if length >= 120:
        return 82
    if length >= 60:
        return 70
    if length >= 25:
        return 58
    if length >= 8:
        return 42
    return 20


def score_number_response(question_key: str, value: float) -> float:
    if question_key == "sales_monthly_target_confidence":
        return max(10, min(value, 10) * 10)

    if question_key == "finance_cash_visibility":
        normalized = min(max(value, 0), 8)
        return 20 + (normalized / 8) * 70

    return max(0, min(value, 100))


def score_answer(question_key: str, value: str | int | float) -> float:
    if isinstance(value, str) and question_key in SELECT_SCORES:
        return float(SELECT_SCORES[question_key].get(value, 35))

    if isinstance(value, (int, float)):
        return round(score_number_response(question_key, float(value)), 2)

    if isinstance(value, str):
        return round(score_text_response(value), 2)

    return 0.0


class AnalysisService:
    """Deterministic V1 scoring and analysis summary generation."""

    def get_analysis(self, user_id: str) -> AnalysisSummaryRead | None:
        return analysis_repository.get(user_id)

    def run_analysis(self, user_id: str) -> AnalysisSummaryRead | None:
        assessment = assessment_service.get_assessment(user_id)
        if assessment is None:
            return None

        section_scores: dict[str, list[float]] = {section.key: [] for section in assessment.sections}

        for answer in assessment.answers:
            section_scores.setdefault(answer.section_key, []).append(
                score_answer(answer.question_key, answer.value)
            )

        category_scores = [
            AnalysisCategoryScore(
                section_key=section.key,
                label=SECTION_LABELS.get(section.key, section.title),
                score=round(
                    sum(section_scores.get(section.key, [])) / max(len(section_scores.get(section.key, [])), 1),
                    2,
                ),
            )
            for section in assessment.sections
        ]

        overall_score = round(
            sum(category.score for category in category_scores) / max(len(category_scores), 1),
            2,
        )

        sorted_desc = sorted(category_scores, key=lambda item: item.score, reverse=True)
        sorted_asc = sorted(category_scores, key=lambda item: item.score)

        top_strengths = [
            f"{category.label} is comparatively strong with a score of {int(round(category.score))}."
            for category in sorted_desc[: min(3, len(sorted_desc))]
        ]

        top_risks = [
            f"{category.label} needs attention with a score of {int(round(category.score))}."
            for category in sorted_asc[: min(3, len(sorted_asc))]
        ]

        top_priorities = [
            PriorityRecommendation(
                title=PRIORITY_RULES[category.section_key]["title"],
                why=PRIORITY_RULES[category.section_key]["why"],
                effort=PRIORITY_RULES[category.section_key]["effort"],
                cost_band=PRIORITY_RULES[category.section_key]["cost_band"],
                expected_impact=PRIORITY_RULES[category.section_key]["expected_impact"],
            )
            for category in sorted_asc[: min(3, len(sorted_asc))]
            if category.section_key in PRIORITY_RULES
        ]

        summary = AnalysisSummaryRead(
            id=f"analysis_{uuid4().hex}",
            assessment_id=assessment.id,
            overall_score=overall_score,
            category_scores=category_scores,
            top_strengths=top_strengths or ["No strengths available yet."],
            top_risks=top_risks or ["No risks available yet."],
            top_priorities=top_priorities or [
                PriorityRecommendation(
                    title="Complete the assessment",
                    why="A more complete assessment gives clearer rule-based recommendations.",
                    effort="low",
                    cost_band="low",
                    expected_impact="medium",
                )
            ],
            created_at=datetime.now(UTC).isoformat(),
            model_version="rule_based_v1",
            workflow_version="analysis_rules_v1",
        )

        return analysis_repository.save(summary, user_id)


analysis_service = AnalysisService()

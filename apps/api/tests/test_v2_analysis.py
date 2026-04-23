from __future__ import annotations

import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch

from fastapi import FastAPI
from fastapi.testclient import TestClient

from app.api.routes.routes_analysis_v2 import router as analysis_v2_router
from app.core.auth import AuthenticatedUser, get_current_user
from app.v2.config import SCALE_LIBRARY
from app.v2.schemas.assessment import (
    AssessmentAnswerRead,
    AssessmentRead,
    AssessmentStatus,
    AssessmentWritePayload,
)
from app.v2.schemas.explainability import ExplainabilitySnapshot
from app.v2.schemas.lifecycle import AnalysisLifecycleState, FreshnessState
from app.v2.schemas.meta import CURRENT_V2_VERSION_METADATA
from app.v2.schemas.profile import BusinessProfileV2Read, ImprovementCapacityPayload
from app.v2.schemas.scoring import (
    AnalysisRunRead,
    AnalysisScoreSummary,
    BucketScore,
    CompletenessSummary,
    ConfidenceLabel,
    CoverageLabel,
    EvidenceConfidenceSummary,
    HealthStatus,
    SectionScore,
)
from app.v2.services.analysis import AnalysisV2Service, MissingSubmittedAssessmentError
from app.v2.services.assessment import AssessmentV2Service
from app.v2.services.scoring import (
    ScoreContext,
    apply_status_caps,
    compute_bucket_score,
    compute_evidence_confidence,
    compute_overall_score,
    compute_section_scores,
    run_deterministic_scoring,
    score_question,
)


def sample_profile(
    *,
    primary_business_type: str = "retail",
    credit_sales_exposure: str = "moderate",
) -> BusinessProfileV2Read:
    return BusinessProfileV2Read(
        id="business_profile_v2_001",
        user_id="user_123",
        created_at="2026-04-23T10:00:00+00:00",
        updated_at="2026-04-23T10:00:00+00:00",
        business_name="BiasharaMind Demo",
        primary_business_type=primary_business_type,
        main_offer="Bookkeeping and growth support",
        customer_type="mixed",
        sales_channels=["walk_in", "whatsapp"],
        fulfilment_model="mixed",
        inventory_involvement="moderate",
        credit_sales_exposure=credit_sales_exposure,
        business_age_stage="established",
        team_size_band="six_to_fifteen",
        number_of_locations=2,
        monthly_revenue_band="5000_to_20000_usd",
        seasonality_level="moderate",
        peak_periods=["weekends"],
        owner_involvement_level="involved_in_key_areas",
        primary_business_goal="grow_sales",
        improvement_capacity=ImprovementCapacityPayload(
            time_capacity="moderate",
            budget_flexibility="tight",
            tool_hire_openness="cautiously_open",
        ),
        record_availability="organized_manual_records",
        compliance_sector_sensitivity="moderate",
    )


class FakeProfileService:
    def __init__(self, profile: BusinessProfileV2Read | None) -> None:
        self.profile = profile

    def get_profile(self, _user_id: str) -> BusinessProfileV2Read | None:
        return self.profile


class FakeAssessmentRepo:
    def __init__(self, assessment: AssessmentRead | None = None) -> None:
        self.assessment = assessment

    def get_latest_submitted(self, _user_id: str) -> AssessmentRead | None:
        return self.assessment


class FakeAnalysisRepository:
    def __init__(self, latest: AnalysisRunRead | None = None) -> None:
        self.latest = latest
        self.created_record = None

    def get_latest(self, _user_id: str) -> AnalysisRunRead | None:
        return self.latest

    def create(self, record):
        self.created_record = record
        payload = record.snapshot_payload
        self.latest = AnalysisRunRead(
            id=record.id,
            analysis_family=record.analysis_family,
            metadata=payload["metadata"],
            lifecycle=payload["lifecycle"],
            summary=payload["deterministicScores"],
            explainability=payload["explainability"],
            created_at="2026-04-23T12:00:00+00:00",
        )
        return self.latest


def question(
    question_id: str,
    *,
    section_id: str,
    question_type: str,
    scale_key: str | None,
    bucket: str,
    essential: bool = True,
    scored: bool = True,
):
    return SimpleNamespace(
        question_id=question_id,
        section_id=section_id,
        question_type=question_type,
        scale_key=scale_key,
        bucket=bucket,
        essential=essential,
        scored=scored,
    )


def answer(
    question_id: str,
    *,
    section_id: str,
    value,
    response_kind: str = "answered",
    is_sufficient_answer: bool = True,
):
    return AssessmentAnswerRead(
        question_id=question_id,
        section_id=section_id,
        module_id=section_id if section_id.endswith("_module") else None,
        answer_type="number" if isinstance(value, (int, float)) else "select",
        response_kind=response_kind,
        value=value,
        is_sufficient_answer=is_sufficient_answer,
        order_index=0,
    )


def build_submitted_assessment(profile: BusinessProfileV2Read) -> AssessmentRead:
    definition_service = AssessmentV2Service(
        assessment_repository=SimpleNamespace(get_latest=lambda _user_id: None),
        analysis_run_repository=SimpleNamespace(mark_stale_due_to_assessment_change=lambda _user_id: 0),
        business_profile_service=FakeProfileService(profile),
    )
    definition = definition_service.build_definition("user_123")
    payload = AssessmentWritePayload(
        answers=[
            {"question_id": "market_offer_clarity", "answer_type": "select", "response_kind": "answered", "value": "well_managed"},
            {"question_id": "revenue_sales_pipeline_repeatability", "answer_type": "select", "response_kind": "answered", "value": "well_managed"},
            {"question_id": "revenue_target_confidence", "answer_type": "number", "response_kind": "answered", "value": 9},
            {"question_id": "customer_follow_up_consistency", "answer_type": "select", "response_kind": "answered", "value": "consistently"},
            {"question_id": "customer_service_issue_visibility", "answer_type": "select", "response_kind": "answered", "value": "strong_visibility"},
            {"question_id": "finance_reporting_rhythm", "answer_type": "select", "response_kind": "answered", "value": "consistently"},
            {"question_id": "finance_cash_position_clarity", "answer_type": "number", "response_kind": "answered", "value": 8},
            {"question_id": "operations_process_stability", "answer_type": "select", "response_kind": "answered", "value": "well_managed"},
            {"question_id": "operations_issue_visibility", "answer_type": "select", "response_kind": "answered", "value": "strong_visibility"},
            {"question_id": "management_priority_clarity", "answer_type": "select", "response_kind": "answered", "value": "well_managed"},
            {"question_id": "management_decision_data_quality", "answer_type": "select", "response_kind": "answered", "value": "strong_visibility"},
            {"question_id": "team_role_coverage", "answer_type": "select", "response_kind": "answered", "value": "well_managed"},
            {"question_id": "team_single_point_dependency", "answer_type": "select", "response_kind": "answered", "value": "no"},
            {"question_id": "risk_cash_pressure_check", "answer_type": "select", "response_kind": "answered", "value": "no"},
            {"question_id": "risk_compliance_exposure_check", "answer_type": "select", "response_kind": "answered", "value": "no"},
            {"question_id": "inventory_accuracy_visibility", "answer_type": "select", "response_kind": "answered", "value": "usable_visibility"},
        ]
    )
    normalized_answers = definition_service.normalize_answers(payload, definition)
    return AssessmentRead(
        id="assessment_v2_001",
        business_profile_v2_id=profile.id,
        question_bank_version=definition.question_bank_version,
        status=AssessmentStatus.SUBMITTED,
        completeness_hint="answered_16_of_18",
        latest_definition_snapshot=definition.model_dump(mode="json", by_alias=True),
        started_at="2026-04-23T10:00:00+00:00",
        submitted_at="2026-04-23T11:00:00+00:00",
        answers=normalized_answers,
    )


def sample_analysis_run() -> AnalysisRunRead:
    return AnalysisRunRead(
        id="analysis_run_v2_001",
        analysis_family="v2_assessment",
        metadata=CURRENT_V2_VERSION_METADATA,
        lifecycle=AnalysisLifecycleState(
            freshness_status=FreshnessState.FRESH,
            diagnosis_state="final",
        ),
        summary=AnalysisScoreSummary(
            overall_health_score=72,
            overall_status=HealthStatus.STABLE_BUT_CONSTRAINED,
            section_scores=[
                SectionScore(
                    section_id="financial_control_cash_discipline",
                    title="Financial Control & Cash Discipline",
                    score=68,
                    bucket_scores=[BucketScore(bucket="outcome", score=70, contributing_question_count=1)],
                    completeness=100,
                    completeness_label=CoverageLabel.HIGH,
                    evidence_confidence=68,
                )
            ],
            completeness=CompletenessSummary(
                overall=92,
                label=CoverageLabel.HIGH,
                essential_answered_sufficiently=12,
                essential_applicable=13,
                optional_answered_sufficiently=4,
                optional_applicable=5,
            ),
            evidence_confidence=EvidenceConfidenceSummary(
                score=68,
                label=ConfidenceLabel.MODERATE,
                specificity=80,
                quantification=60,
                internal_consistency=75,
                corroboration=58,
                key_limitations=["Some sections still have light corroborating evidence."],
            ),
            active_critical_risk_count=0,
            caps_applied=[],
        ),
        explainability=ExplainabilitySnapshot(),
        created_at="2026-04-23T12:00:00+00:00",
    )


class ScoringHelpersTests(unittest.TestCase):
    def test_question_level_scoring_handles_structured_numeric_and_unknown(self) -> None:
        scale_map = {scale.key: scale for scale in SCALE_LIBRARY}
        select_question = question(
            "market_offer_clarity",
            section_id="market_offer_strength",
            question_type="select",
            scale_key="maturity_4",
            bucket="outcome",
        )
        number_question = question(
            "revenue_target_confidence",
            section_id="revenue_engine",
            question_type="number",
            scale_key="numeric_0_10",
            bucket="outcome",
        )
        answered_select = answer("market_offer_clarity", section_id="market_offer_strength", value="well_managed")
        answered_number = answer("revenue_target_confidence", section_id="revenue_engine", value=7.0)
        unknown_answer = AssessmentAnswerRead(
            question_id="revenue_target_confidence",
            section_id="revenue_engine",
            module_id=None,
            answer_type="number",
            response_kind="unknown",
            value=None,
            is_sufficient_answer=False,
            order_index=1,
        )

        self.assertEqual(score_question(answered_select, select_question, scale_map), 85.0)
        self.assertEqual(score_question(answered_number, number_question, scale_map), 70.0)
        self.assertIsNone(score_question(unknown_answer, number_question, scale_map))

    def test_bucket_reweighting_only_uses_available_buckets(self) -> None:
        score, bucket_scores = compute_bucket_score({"outcome": [80], "control": [], "risk": [40]})

        self.assertAlmostEqual(score, 67.69, places=2)
        self.assertEqual(len(bucket_scores), 3)
        self.assertEqual(bucket_scores[1].contributing_question_count, 0)

    def test_section_scoring_blends_adaptive_module_at_thirty_percent(self) -> None:
        context = ScoreContext(
            answers=[
                answer("operations_process_stability", section_id="operations_delivery_reliability", value="well_managed"),
                answer("operations_issue_visibility", section_id="operations_delivery_reliability", value="strong_visibility"),
                answer("inventory_accuracy_visibility", section_id="inventory_stock_control_module", value="not_visible"),
            ],
            question_map={
                "operations_process_stability": question(
                    "operations_process_stability",
                    section_id="operations_delivery_reliability",
                    question_type="select",
                    scale_key="maturity_4",
                    bucket="control",
                ),
                "operations_issue_visibility": question(
                    "operations_issue_visibility",
                    section_id="operations_delivery_reliability",
                    question_type="select",
                    scale_key="coverage_4",
                    bucket="outcome",
                ),
                "inventory_accuracy_visibility": question(
                    "inventory_accuracy_visibility",
                    section_id="inventory_stock_control_module",
                    question_type="select",
                    scale_key="coverage_4",
                    bucket="control",
                ),
            },
            section_titles={"operations_delivery_reliability": "Operations & Delivery Reliability"},
            module_parent_map={"inventory_stock_control_module": "operations_delivery_reliability"},
            section_question_ids={
                "operations_delivery_reliability": ["operations_process_stability", "operations_issue_visibility"],
                "inventory_stock_control_module": ["inventory_accuracy_visibility"],
            },
        )

        section = compute_section_scores(context, {"operations_delivery_reliability": 100, "inventory_stock_control_module": 100})[0]

        self.assertAlmostEqual(section.module_contribution_score or 0, 20.0, places=2)
        self.assertAlmostEqual(section.module_contribution_weight or 0, 0.3, places=2)
        self.assertAlmostEqual(section.score, 65.5, places=2)

    def test_overall_score_and_caps_follow_finalized_rules(self) -> None:
        section_scores = [
            SectionScore(section_id="market_offer_strength", title="Market", score=85, bucket_scores=[], completeness=90, completeness_label=CoverageLabel.HIGH, evidence_confidence=70),
            SectionScore(section_id="revenue_engine", title="Revenue", score=85, bucket_scores=[], completeness=90, completeness_label=CoverageLabel.HIGH, evidence_confidence=70),
            SectionScore(section_id="customer_retention_service_quality", title="Customer", score=85, bucket_scores=[], completeness=90, completeness_label=CoverageLabel.HIGH, evidence_confidence=70),
            SectionScore(section_id="financial_control_cash_discipline", title="Finance", score=20, bucket_scores=[], completeness=90, completeness_label=CoverageLabel.HIGH, evidence_confidence=70),
            SectionScore(section_id="operations_delivery_reliability", title="Operations", score=85, bucket_scores=[], completeness=90, completeness_label=CoverageLabel.HIGH, evidence_confidence=70),
            SectionScore(section_id="management_control_planning_discipline", title="Management", score=85, bucket_scores=[], completeness=90, completeness_label=CoverageLabel.HIGH, evidence_confidence=70),
            SectionScore(section_id="team_capacity_continuity", title="Team", score=85, bucket_scores=[], completeness=90, completeness_label=CoverageLabel.HIGH, evidence_confidence=70),
        ]

        overall = compute_overall_score(section_scores)
        status, caps, provisional, _ = apply_status_caps(overall, section_scores, active_critical_risk_count=0)

        self.assertAlmostEqual(overall, 69.4, places=2)
        self.assertEqual(status, HealthStatus.VULNERABLE)
        self.assertTrue(any(cap.code == "financial_control_cap" for cap in caps))
        self.assertFalse(provisional)

    def test_unknown_answers_do_not_collapse_health_to_zero_and_low_key_coverage_is_provisional(self) -> None:
        context = ScoreContext(
            answers=[
                answer("revenue_target_confidence", section_id="revenue_engine", value=9.0),
                AssessmentAnswerRead(
                    question_id="finance_cash_position_clarity",
                    section_id="financial_control_cash_discipline",
                    module_id=None,
                    answer_type="number",
                    response_kind="unknown",
                    value=None,
                    is_sufficient_answer=False,
                    order_index=1,
                ),
            ],
            question_map={
                "revenue_target_confidence": question(
                    "revenue_target_confidence",
                    section_id="revenue_engine",
                    question_type="number",
                    scale_key="numeric_0_10",
                    bucket="outcome",
                ),
                "finance_cash_position_clarity": question(
                    "finance_cash_position_clarity",
                    section_id="financial_control_cash_discipline",
                    question_type="number",
                    scale_key="numeric_0_10",
                    bucket="outcome",
                ),
            },
            section_titles={
                "revenue_engine": "Revenue Engine",
                "financial_control_cash_discipline": "Financial Control & Cash Discipline",
            },
            module_parent_map={},
            section_question_ids={
                "revenue_engine": ["revenue_target_confidence"],
                "financial_control_cash_discipline": ["finance_cash_position_clarity"],
            },
        )

        summary, _, lifecycle = run_deterministic_scoring(context)

        self.assertGreater(summary.overall_health_score, 0)
        self.assertEqual(lifecycle.freshness_status, FreshnessState.PROVISIONAL)
        self.assertEqual(lifecycle.diagnosis_state, "provisional")

    def test_evidence_confidence_uses_deterministic_contradiction_signals(self) -> None:
        context = ScoreContext(
            answers=[
                answer("risk_cash_pressure_check", section_id="critical_risk_checks", value="yes"),
                answer("finance_cash_position_clarity", section_id="financial_control_cash_discipline", value=9.0),
                answer("team_single_point_dependency", section_id="team_capacity_continuity", value="yes"),
                answer("team_role_coverage", section_id="team_capacity_continuity", value="well_managed"),
            ],
            question_map={
                "risk_cash_pressure_check": question("risk_cash_pressure_check", section_id="critical_risk_checks", question_type="select", scale_key="yes_no", bucket="risk", scored=False),
                "finance_cash_position_clarity": question("finance_cash_position_clarity", section_id="financial_control_cash_discipline", question_type="number", scale_key="numeric_0_10", bucket="outcome"),
                "team_single_point_dependency": question("team_single_point_dependency", section_id="team_capacity_continuity", question_type="select", scale_key="yes_no", bucket="risk"),
                "team_role_coverage": question("team_role_coverage", section_id="team_capacity_continuity", question_type="select", scale_key="maturity_4", bucket="control"),
            },
            section_titles={
                "financial_control_cash_discipline": "Financial Control",
                "team_capacity_continuity": "Team Capacity",
            },
            module_parent_map={},
            section_question_ids={
                "financial_control_cash_discipline": ["finance_cash_position_clarity"],
                "team_capacity_continuity": ["team_single_point_dependency", "team_role_coverage"],
            },
        )

        confidence = compute_evidence_confidence(context, {"financial_control_cash_discipline": 100, "team_capacity_continuity": 100})

        self.assertEqual(confidence.internal_consistency, 40.0)
        self.assertIn("Some answers appear internally inconsistent.", confidence.key_limitations)


class AnalysisServiceTests(unittest.TestCase):
    def test_analysis_service_persists_snapshot_payload_and_returns_serializable_output(self) -> None:
        profile = sample_profile()
        assessment = build_submitted_assessment(profile)
        repository = FakeAnalysisRepository()
        service = AnalysisV2Service(
            analysis_repository=repository,
            assessment_repository=FakeAssessmentRepo(assessment),
            business_profile_service=FakeProfileService(profile),
        )

        result = service.run_analysis("user_123")
        dumped = result.model_dump(mode="json", by_alias=True)

        self.assertIsNotNone(repository.created_record)
        self.assertEqual(repository.created_record.analysis_family, "v2_assessment")
        self.assertEqual(repository.created_record.business_profile_v2_id, profile.id)
        self.assertEqual(repository.created_record.assessment_v2_id, assessment.id)
        self.assertIn("profileSnapshot", repository.created_record.snapshot_payload)
        self.assertIn("assessmentSnapshot", repository.created_record.snapshot_payload)
        self.assertIn("deterministicScores", repository.created_record.snapshot_payload)
        self.assertIn("overallHealthScore", dumped["summary"])


class AnalysisV2RouteTests(unittest.TestCase):
    def setUp(self) -> None:
        self.app = FastAPI()
        self.app.include_router(analysis_v2_router)
        self.app.dependency_overrides[get_current_user] = lambda: AuthenticatedUser(id="user_123", email="user@example.com")
        self.client = TestClient(self.app)

    def tearDown(self) -> None:
        self.app.dependency_overrides.clear()

    def test_authentication_is_required(self) -> None:
        app_without_override = FastAPI()
        app_without_override.include_router(analysis_v2_router)
        client = TestClient(app_without_override)

        response = client.get("/v2/analysis")

        self.assertEqual(response.status_code, 401)

    def test_routes_return_latest_analysis_and_run_results(self) -> None:
        class FakeService:
            def get_latest(self, _user_id: str):
                return sample_analysis_run()

            def run_analysis(self, _user_id: str):
                return sample_analysis_run()

        with patch("app.api.routes.routes_analysis_v2.get_analysis_v2_service", return_value=FakeService()):
            get_response = self.client.get("/v2/analysis")
            run_response = self.client.post("/v2/analysis/run")

        self.assertEqual(get_response.status_code, 200)
        self.assertEqual(run_response.status_code, 200)
        self.assertEqual(get_response.json()["summary"]["overallStatus"], "stable_but_constrained")

    def test_missing_submitted_assessment_returns_clear_validation_response(self) -> None:
        class MissingInputsService:
            def get_latest(self, _user_id: str):
                return None

            def run_analysis(self, _user_id: str):
                raise MissingSubmittedAssessmentError("Submit the V2 assessment before running V2 analysis.")

        with patch("app.api.routes.routes_analysis_v2.get_analysis_v2_service", return_value=MissingInputsService()):
            response = self.client.post("/v2/analysis/run")

        self.assertEqual(response.status_code, 409)
        self.assertIn("assessment", response.json()["detail"])


class V1CoexistenceTests(unittest.TestCase):
    def test_v1_analysis_route_file_remains_present(self) -> None:
        route_file = Path("apps/api/app/api/routes/routes_analysis.py")
        content = route_file.read_text(encoding="utf-8")

        self.assertIn('@router.get("/analysis"', content)
        self.assertIn('@router.post("/analysis/run"', content)


if __name__ == "__main__":
    unittest.main()

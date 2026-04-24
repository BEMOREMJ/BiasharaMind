from __future__ import annotations

import unittest
from types import SimpleNamespace
from unittest.mock import patch

from app.v2.schemas.assessment import AssessmentRead, AssessmentStatus, AssessmentWritePayload
from app.v2.schemas.interpretation import EvidenceSpecificity
from app.v2.services.ai_interpretation import AITextInterpretationService
from app.v2.services.analysis import AnalysisV2Service
from app.v2.services.assessment import AssessmentV2Service
from app.v2.prompts.interpretation import build_text_interpretation_prompt


class StubProvider:
    provider_name = "stub"

    def __init__(self, response: str | Exception) -> None:
        self.response = response
        self.prompts: list[str] = []

    def generate_structured_json(self, *, system_prompt: str, user_prompt: str) -> str:
        self.prompts.append(user_prompt)
        if isinstance(self.response, Exception):
            raise self.response
        return self.response


class FakeProfileService:
    def __init__(self, profile) -> None:
        self.profile = profile

    def get_profile(self, _user_id: str):
        return self.profile


class FakeAssessmentRepo:
    def __init__(self, assessment: AssessmentRead) -> None:
        self.assessment = assessment

    def get_latest_submitted(self, _user_id: str) -> AssessmentRead:
        return self.assessment


class FakeAnalysisRepository:
    def __init__(self) -> None:
        self.created = None

    def get_latest(self, _user_id: str):
        return None

    def create(self, record):
        self.created = record
        payload = record.snapshot_payload
        from app.v2.schemas.scoring import AnalysisRunRead

        return AnalysisRunRead(
            id=record.id,
            analysis_family=record.analysis_family,
            metadata=payload["metadata"],
            lifecycle=payload["lifecycle"],
            summary=payload["deterministicScores"],
            critical_risks=payload["criticalRisks"],
            diagnosis=payload["diagnosis"],
            issue_candidates=payload["issueCandidates"],
            top_priorities=payload["topPriorities"],
            watchlist=payload["watchlist"],
            roadmap_inputs=payload["roadmapInputs"],
            text_interpretation=payload["textInterpretation"],
            explainability=payload["explainability"],
            created_at="2026-04-24T10:00:00+00:00",
        )


def sample_profile():
    from app.v2.schemas.profile import BusinessProfileV2Read, ImprovementCapacityPayload

    return BusinessProfileV2Read(
        id="business_profile_v2_001",
        user_id="user_123",
        created_at="2026-04-24T09:00:00+00:00",
        updated_at="2026-04-24T09:00:00+00:00",
        business_name="BiasharaMind Demo",
        primary_business_type="retail",
        main_offer="Retail support",
        customer_type="mixed",
        sales_channels=["walk_in", "whatsapp"],
        fulfilment_model="mixed",
        inventory_involvement="moderate",
        credit_sales_exposure="moderate",
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


def build_submitted_assessment():
    profile = sample_profile()
    definition_service = AssessmentV2Service(
        assessment_repository=SimpleNamespace(get_latest=lambda _user_id: None),
        analysis_run_repository=SimpleNamespace(mark_stale_due_to_assessment_change=lambda _user_id: 0),
        business_profile_service=FakeProfileService(profile),
    )
    definition = definition_service.build_definition("user_123")
    payload = AssessmentWritePayload(
        answers=[
            {"question_id": "market_offer_clarity", "answer_type": "select", "response_kind": "answered", "value": "partly_defined"},
            {"question_id": "revenue_sales_pipeline_repeatability", "answer_type": "select", "response_kind": "answered", "value": "ad_hoc"},
            {"question_id": "revenue_target_confidence", "answer_type": "number", "response_kind": "answered", "value": 4},
            {"question_id": "finance_reporting_rhythm", "answer_type": "select", "response_kind": "answered", "value": "sometimes"},
            {"question_id": "finance_cash_position_clarity", "answer_type": "number", "response_kind": "answered", "value": 3},
            {"question_id": "risk_cash_pressure_check", "answer_type": "select", "response_kind": "answered", "value": "yes"},
            {"question_id": "operations_process_stability", "answer_type": "select", "response_kind": "answered", "value": "ad_hoc"},
            {"question_id": "operations_issue_visibility", "answer_type": "select", "response_kind": "answered", "value": "basic_visibility"},
            {"question_id": "customer_follow_up_consistency", "answer_type": "select", "response_kind": "answered", "value": "sometimes"},
            {"question_id": "customer_service_issue_visibility", "answer_type": "select", "response_kind": "answered", "value": "basic_visibility"},
            {"question_id": "management_priority_clarity", "answer_type": "select", "response_kind": "answered", "value": "ad_hoc"},
            {"question_id": "management_decision_data_quality", "answer_type": "select", "response_kind": "answered", "value": "basic_visibility"},
            {"question_id": "team_role_coverage", "answer_type": "select", "response_kind": "answered", "value": "ad_hoc"},
            {"question_id": "team_single_point_dependency", "answer_type": "select", "response_kind": "answered", "value": "yes"},
            {"question_id": "finance_surprise_notes", "answer_type": "textarea", "response_kind": "answered", "value": "We say cash is fine, but every month we scramble to cover supplier payments and delay follow-up on collections."},
            {"question_id": "operations_reliability_notes", "answer_type": "textarea", "response_kind": "answered", "value": "Orders get delayed when stock numbers are off and nobody catches the issue until customers complain."},
        ]
    )
    normalized = definition_service.normalize_answers(payload, definition)
    return profile, AssessmentRead(
        id="assessment_v2_001",
        business_profile_v2_id=profile.id,
        question_bank_version=definition.question_bank_version,
        status=AssessmentStatus.SUBMITTED,
        completeness_hint="answered_16_of_18",
        latest_definition_snapshot=definition.model_dump(mode="json", by_alias=True),
        started_at="2026-04-24T09:00:00+00:00",
        submitted_at="2026-04-24T09:30:00+00:00",
        answers=normalized,
    )


class AIInterpretationServiceTests(unittest.TestCase):
    def test_prompt_builder_contains_grounding_inputs(self) -> None:
        prompt = build_text_interpretation_prompt(
            {
                "question_key": "finance_surprise_notes",
                "section_key": "financial_control_cash_discipline",
                "question_prompt": "What kinds of cash or reporting surprises still catch the business off guard?",
                "answer_text": "We scramble for payments every month.",
                "business_profile_context": {"primary_business_type": "retail"},
                "supporting_structured_answers": [{"question_id": "finance_cash_position_clarity", "value": 3}],
            }
        )

        self.assertIn("finance_surprise_notes", prompt)
        self.assertIn("supporting_structured_answers", prompt)
        self.assertIn("strict JSON", build_text_interpretation_prompt.__globals__["INTERPRETATION_SYSTEM_PROMPT"])

    def test_valid_structured_interpretation_parses(self) -> None:
        profile, assessment = build_submitted_assessment()
        provider = StubProvider(
            """
            {
              "question_key": "finance_surprise_notes",
              "section_key": "financial_control_cash_discipline",
              "summary": "Cash surprises are recurring and tied to weak collections follow-up.",
              "issue_tags": [{"code": "FINANCE_VISIBILITY_GAP", "label": "Finance visibility gap", "confidence": 0.84}],
              "root_cause_tags": [{"code": "collections_delay", "label": "Collections delay", "confidence": 0.76}],
              "affected_dimensions": ["finance"],
              "severity_hint": "high",
              "contradiction_flags": [{"code": "cash_visibility_contradiction", "detail": "The text describes recurring cash scrambles while structured cash clarity is low.", "severity": "high", "source_refs": ["finance_surprise_notes", "finance_cash_position_clarity"]}],
              "evidence_specificity": "high",
              "evidence_strength": "strong",
              "interpretation_confidence": "high",
              "evidence_snippets": ["every month we scramble to cover supplier payments"],
              "fallback": {"used": false, "partial": false, "recoverable": true}
            }
            """
        )
        service = AITextInterpretationService(provider=provider)
        snapshot = service.interpret(
            profile=profile,
            assessment=assessment,
            question_map={
                question["questionId"]: SimpleNamespace(
                    question_type=question["questionType"],
                    interpretation_enabled=question.get("interpretationEnabled", False),
                    prompt=question["prompt"],
                    tags=question.get("tags", []),
                )
                for section in assessment.latest_definition_snapshot["sections"]
                for question in section["questions"]
            },
        )

        self.assertEqual(snapshot.status, "partial")
        self.assertTrue(any(output.question_key == "finance_surprise_notes" for output in snapshot.outputs))
        finance_output = [output for output in snapshot.outputs if output.question_key == "finance_surprise_notes"][0]
        self.assertEqual(finance_output.evidence_specificity, EvidenceSpecificity.HIGH)
        self.assertEqual(finance_output.contradiction_flags[0].source_refs[0], "finance_surprise_notes")

    def test_invalid_json_uses_fallback(self) -> None:
        profile, assessment = build_submitted_assessment()
        service = AITextInterpretationService(provider=StubProvider("not-json"))
        snapshot = service.interpret(
            profile=profile,
            assessment=assessment,
            question_map={
                question["questionId"]: SimpleNamespace(
                    question_type=question["questionType"],
                    interpretation_enabled=question.get("interpretationEnabled", False),
                    prompt=question["prompt"],
                    tags=question.get("tags", []),
                )
                for section in assessment.latest_definition_snapshot["sections"]
                for question in section["questions"]
            },
        )

        self.assertEqual(snapshot.status, "fallback_used")
        self.assertTrue(all(output.fallback.used for output in snapshot.outputs))

    def test_missing_fields_use_fallback(self) -> None:
        profile, assessment = build_submitted_assessment()
        provider = StubProvider('{"section_key":"financial_control_cash_discipline"}')
        service = AITextInterpretationService(provider=provider)
        snapshot = service.interpret(
            profile=profile,
            assessment=assessment,
            question_map={
                question["questionId"]: SimpleNamespace(
                    question_type=question["questionType"],
                    interpretation_enabled=question.get("interpretationEnabled", False),
                    prompt=question["prompt"],
                    tags=question.get("tags", []),
                )
                for section in assessment.latest_definition_snapshot["sections"]
                for question in section["questions"]
            },
        )

        self.assertTrue(snapshot.outputs[0].fallback.used)
        self.assertIsNotNone(snapshot.outputs[0].fallback.reason)


class AnalysisIntegrationTests(unittest.TestCase):
    def test_analysis_succeeds_and_score_is_unchanged_when_ai_fails(self) -> None:
        profile, assessment = build_submitted_assessment()
        repository_a = FakeAnalysisRepository()
        repository_b = FakeAnalysisRepository()
        service_a = AnalysisV2Service(
            analysis_repository=repository_a,
            assessment_repository=FakeAssessmentRepo(assessment),
            business_profile_service=FakeProfileService(profile),
        )
        service_b = AnalysisV2Service(
            analysis_repository=repository_b,
            assessment_repository=FakeAssessmentRepo(assessment),
            business_profile_service=FakeProfileService(profile),
        )

        valid_provider = StubProvider(
            """
            {"question_key":"finance_surprise_notes","section_key":"financial_control_cash_discipline","summary":"Recurring cash scrambles are linked to weak collections discipline.","issue_tags":[],"root_cause_tags":[],"affected_dimensions":["finance"],"severity_hint":"high","contradiction_flags":[],"evidence_specificity":"medium","evidence_strength":"mixed","interpretation_confidence":"medium","evidence_snippets":["scramble to cover supplier payments"],"fallback":{"used":false,"partial":false,"recoverable":true}}
            """
        )
        fail_provider = StubProvider(Exception("provider offline"))

        with patch("app.v2.services.analysis.get_ai_text_interpretation_service", return_value=AITextInterpretationService(provider=valid_provider)):
            success_run = service_a.run_analysis("user_123")
        with patch("app.v2.services.analysis.get_ai_text_interpretation_service", return_value=AITextInterpretationService(provider=fail_provider)):
            fallback_run = service_b.run_analysis("user_123")

        self.assertEqual(success_run.summary.overall_health_score, fallback_run.summary.overall_health_score)
        self.assertEqual(fallback_run.text_interpretation.status, "fallback_used")
        self.assertIn("textInterpretation", repository_b.created.snapshot_payload)
        self.assertTrue(any(output.fallback.used for output in fallback_run.text_interpretation.outputs))

    def test_contradiction_flags_persist_into_analysis_and_lifecycle(self) -> None:
        profile, assessment = build_submitted_assessment()
        repository = FakeAnalysisRepository()
        service = AnalysisV2Service(
            analysis_repository=repository,
            assessment_repository=FakeAssessmentRepo(assessment),
            business_profile_service=FakeProfileService(profile),
        )
        provider = StubProvider(
            """
            {"question_key":"finance_surprise_notes","section_key":"financial_control_cash_discipline","summary":"The text conflicts with the current cash-control narrative.","issue_tags":[],"root_cause_tags":[],"affected_dimensions":["finance"],"severity_hint":"high","contradiction_flags":[{"code":"cash_visibility_contradiction","detail":"Narrative says cash is fine while the answer describes monthly scrambles.","severity":"high","source_refs":["finance_surprise_notes","finance_cash_position_clarity"]}],"evidence_specificity":"high","evidence_strength":"strong","interpretation_confidence":"high","evidence_snippets":["every month we scramble"],"fallback":{"used":false,"partial":false,"recoverable":true}}
            """
        )

        with patch("app.v2.services.analysis.get_ai_text_interpretation_service", return_value=AITextInterpretationService(provider=provider)):
            run = service.run_analysis("user_123")

        self.assertEqual(run.lifecycle.ai_interpretation_status, "partial")
        self.assertTrue(any(limit.code == "cash_visibility_contradiction" for limit in run.explainability.confidence_limitations))
        self.assertTrue(any(output.contradiction_flags for output in run.text_interpretation.outputs))


if __name__ == "__main__":
    unittest.main()

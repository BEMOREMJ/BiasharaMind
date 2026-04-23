from __future__ import annotations

import unittest
from pathlib import Path
from unittest.mock import patch

from fastapi import FastAPI
from fastapi.testclient import TestClient

from app.api.routes.routes_assessment_v2 import router as assessment_v2_router
from app.core.auth import AuthenticatedUser, get_current_user
from app.v2.schemas.assessment import (
    AssessmentRead,
    AssessmentSaveResponse,
    AssessmentStatus,
    AssessmentWritePayload,
    ResponseKind,
)
from app.v2.schemas.profile import (
    BusinessProfileV2Read,
    ImprovementCapacityPayload,
)
from app.v2.services.assessment import AssessmentV2Service, MissingBusinessProfileError


def sample_profile(
    *,
    primary_business_type: str = "retail",
    credit_sales_exposure: str = "low",
) -> BusinessProfileV2Read:
    return BusinessProfileV2Read(
        id="business_profile_v2_001",
        user_id="user_123",
        created_at="2026-04-23T10:00:00+00:00",
        updated_at="2026-04-23T10:00:00+00:00",
        business_name="BiasharaMind Demo",
        primary_business_type=primary_business_type,
        main_offer="Demo offer",
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
    def __init__(self) -> None:
        self.saved: AssessmentRead | None = None

    def get_latest(self, _user_id: str) -> AssessmentRead | None:
        return self.saved

    def save(self, assessment: AssessmentRead, _user_id: str) -> AssessmentRead:
        self.saved = assessment
        return assessment


class FakeAnalysisRunRepo:
    def __init__(self, stale_count: int = 0) -> None:
        self.stale_count = stale_count
        self.assessment_change_calls = 0

    def mark_stale_due_to_assessment_change(self, _user_id: str) -> int:
        self.assessment_change_calls += 1
        return self.stale_count


class AssessmentV2ServiceTests(unittest.TestCase):
    def test_module_selection_matches_expected_profile_triggers(self) -> None:
        service = AssessmentV2Service(
            assessment_repository=FakeAssessmentRepo(),
            analysis_run_repository=FakeAnalysisRunRepo(),
            business_profile_service=FakeProfileService(sample_profile(primary_business_type="retail")),
        )
        retail_modules = [module.key for module in service.select_applicable_modules(sample_profile(primary_business_type="retail"))]
        service_modules = [module.key for module in service.select_applicable_modules(sample_profile(primary_business_type="services"))]
        manufacturing_modules = [module.key for module in service.select_applicable_modules(sample_profile(primary_business_type="manufacturing"))]
        credit_modules = [module.key for module in service.select_applicable_modules(sample_profile(credit_sales_exposure="high"))]

        self.assertIn("inventory_stock_control", retail_modules)
        self.assertIn("service_capacity_scheduling", service_modules)
        self.assertIn("production_process_reliability", manufacturing_modules)
        self.assertIn("credit_collections", credit_modules)

    def test_definition_assembly_uses_core_sections_and_adaptive_modules(self) -> None:
        service = AssessmentV2Service(
            assessment_repository=FakeAssessmentRepo(),
            analysis_run_repository=FakeAnalysisRunRepo(),
            business_profile_service=FakeProfileService(sample_profile(primary_business_type="retail")),
        )

        definition = service.build_definition("user_123")

        self.assertEqual(len([section for section in definition.sections if section.is_core]), 8)
        self.assertTrue(any(module.module_id == "inventory_stock_control" for module in definition.adaptive_modules))
        self.assertGreater(definition.total_questions, 8)

    def test_answer_validation_and_normalization(self) -> None:
        service = AssessmentV2Service(
            assessment_repository=FakeAssessmentRepo(),
            analysis_run_repository=FakeAnalysisRunRepo(),
            business_profile_service=FakeProfileService(sample_profile()),
        )
        definition = service.build_definition("user_123")
        payload = AssessmentWritePayload(
            answers=[
                {
                    "question_id": "market_offer_clarity",
                    "answer_type": "select",
                    "response_kind": "answered",
                    "value": "partly_defined",
                },
                {
                    "question_id": "revenue_target_confidence",
                    "answer_type": "number",
                    "response_kind": "answered",
                    "value": 7,
                },
                {
                    "question_id": "market_customer_signal_sources",
                    "answer_type": "multiselect",
                    "response_kind": "answered",
                    "value": ["walk_in", "whatsapp"],
                },
                {
                    "question_id": "risk_compliance_exposure_check",
                    "answer_type": "select",
                    "response_kind": "prefer_not_to_say",
                    "value": None,
                },
            ]
        )

        normalized = service.normalize_answers(payload, definition)

        self.assertEqual(normalized[0].section_id, "market_offer_strength")
        self.assertEqual(normalized[1].value, 7.0)
        self.assertEqual(normalized[2].value, ["walk_in", "whatsapp"])
        self.assertEqual(normalized[3].response_kind, ResponseKind.PREFER_NOT_TO_SAY)
        self.assertFalse(normalized[3].is_sufficient_answer)

    def test_save_and_submit_persist_and_mark_stale_when_existing_assessment_changes(self) -> None:
        assessment_repo = FakeAssessmentRepo()
        analysis_repo = FakeAnalysisRunRepo(stale_count=2)
        service = AssessmentV2Service(
            assessment_repository=assessment_repo,
            analysis_run_repository=analysis_repo,
            business_profile_service=FakeProfileService(sample_profile()),
        )
        save_payload = AssessmentWritePayload(
            answers=[
                {
                    "question_id": "market_offer_clarity",
                    "answer_type": "select",
                    "response_kind": "answered",
                    "value": "well_managed",
                }
            ]
        )

        first_save = service.save_assessment(save_payload, "user_123")
        submit_result = service.submit_assessment(save_payload, "user_123")

        self.assertEqual(first_save.assessment.status, AssessmentStatus.DRAFT)
        self.assertEqual(first_save.analysis_impact.stale_analysis_runs, 0)
        self.assertEqual(submit_result.assessment.status, AssessmentStatus.SUBMITTED)
        self.assertEqual(submit_result.analysis_impact.stale_analysis_runs, 2)
        self.assertEqual(analysis_repo.assessment_change_calls, 1)

    def test_missing_profile_blocks_definition(self) -> None:
        service = AssessmentV2Service(
            assessment_repository=FakeAssessmentRepo(),
            analysis_run_repository=FakeAnalysisRunRepo(),
            business_profile_service=FakeProfileService(None),
        )

        with self.assertRaises(MissingBusinessProfileError):
            service.build_definition("user_123")


class AssessmentV2RouteTests(unittest.TestCase):
    def setUp(self) -> None:
        self.app = FastAPI()
        self.app.include_router(assessment_v2_router)
        self.app.dependency_overrides[get_current_user] = lambda: AuthenticatedUser(id="user_123", email="user@example.com")
        self.client = TestClient(self.app)

    def tearDown(self) -> None:
        self.app.dependency_overrides.clear()

    def test_authentication_is_required(self) -> None:
        app_without_override = FastAPI()
        app_without_override.include_router(assessment_v2_router)
        client = TestClient(app_without_override)

        response = client.get("/v2/assessment/definition")

        self.assertEqual(response.status_code, 401)

    def test_routes_return_definition_save_and_submit(self) -> None:
        class FakeService:
            def build_definition(self, _user_id: str):
                return AssessmentV2Service(
                    assessment_repository=FakeAssessmentRepo(),
                    analysis_run_repository=FakeAnalysisRunRepo(),
                    business_profile_service=FakeProfileService(sample_profile()),
                ).build_definition("user_123")

            def get_assessment(self, _user_id: str):
                return None

            def save_assessment(self, _payload, _user_id: str):
                return AssessmentSaveResponse(
                    assessment=AssessmentRead(
                        id="assessment_v2_001",
                        business_profile_v2_id="business_profile_v2_001",
                        question_bank_version="v2.0.0",
                        status="draft",
                        completeness_hint="answered_1_of_26",
                        latest_definition_snapshot={"sections": []},
                        started_at="2026-04-23T10:00:00+00:00",
                        submitted_at=None,
                        answers=[],
                    ),
                    analysis_impact={"stale_analysis_runs": 1, "rerun_required": True, "message": "rerun"},
                )

            def submit_assessment(self, _payload, _user_id: str):
                return self.save_assessment(_payload, _user_id)

        with patch("app.api.routes.routes_assessment_v2.get_assessment_v2_service", return_value=FakeService()):
            definition_response = self.client.get("/v2/assessment/definition")
            save_response = self.client.put(
                "/v2/assessment",
                json={"answers": [{"questionId": "market_offer_clarity", "answerType": "select", "responseKind": "answered", "value": "well_managed"}]},
            )
            submit_response = self.client.post(
                "/v2/assessment/submit",
                json={"answers": [{"questionId": "market_offer_clarity", "answerType": "select", "responseKind": "answered", "value": "well_managed"}]},
            )

        self.assertEqual(definition_response.status_code, 200)
        self.assertEqual(save_response.status_code, 200)
        self.assertEqual(submit_response.status_code, 200)
        self.assertTrue(save_response.json()["analysisImpact"]["rerunRequired"])

    def test_missing_profile_returns_clear_validation_response(self) -> None:
        class MissingProfileService:
            def build_definition(self, _user_id: str):
                raise MissingBusinessProfileError("Complete the V2 business profile before starting the V2 assessment.")

        with patch("app.api.routes.routes_assessment_v2.get_assessment_v2_service", return_value=MissingProfileService()):
            response = self.client.get("/v2/assessment/definition")

        self.assertEqual(response.status_code, 409)
        self.assertIn("business profile", response.json()["detail"])


class V1CoexistenceTests(unittest.TestCase):
    def test_v1_assessment_route_file_remains_present(self) -> None:
        route_file = Path("apps/api/app/api/routes/routes_assessment.py")
        content = route_file.read_text(encoding="utf-8")

        self.assertIn('@router.get("/assessment"', content)
        self.assertIn('@router.post("/assessment/submit"', content)


if __name__ == "__main__":
    unittest.main()

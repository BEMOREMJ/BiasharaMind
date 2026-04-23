from __future__ import annotations

import unittest
from datetime import UTC, datetime
from unittest.mock import patch

from fastapi import FastAPI
from fastapi.testclient import TestClient

from app.core.auth import AuthenticatedUser, get_current_user
from app.api.routes.routes_business_profile_v2 import router as business_profile_v2_router
from app.v2.schemas.profile import (
    BusinessProfileV2Create,
    BusinessProfileV2Read,
    BusinessProfileV2SaveResponse,
    ImprovementCapacityPayload,
)
from app.v2.services.business_profile import BusinessProfileV2Service


def sample_payload() -> BusinessProfileV2Create:
    return BusinessProfileV2Create(
        business_name="BiasharaMind Foods",
        primary_business_type="food_and_hospitality",
        main_offer="Prepared meals and event catering",
        customer_type="mixed",
        sales_channels=["walk_in", "whatsapp", "referrals"],
        fulfilment_model="mixed",
        inventory_involvement="moderate",
        credit_sales_exposure="low",
        business_age_stage="established",
        team_size_band="six_to_fifteen",
        number_of_locations=2,
        monthly_revenue_band="5000_to_20000_usd",
        seasonality_level="moderate",
        peak_periods=["holiday_periods", "weekends"],
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


def sample_read_model() -> BusinessProfileV2Read:
    return BusinessProfileV2Read(
        id="business_profile_v2_existing",
        user_id="user_123",
        created_at=datetime.now(UTC).isoformat(),
        updated_at=datetime.now(UTC).isoformat(),
        **sample_payload().model_dump(),
    )


class BusinessProfileV2SchemaTests(unittest.TestCase):
    def test_schema_validation_normalizes_multi_selects(self) -> None:
        payload = BusinessProfileV2Create.model_validate(
            sample_payload().model_dump()
            | {
                "sales_channels": ["walk_in", " walk_in ", "whatsapp"],
                "peak_periods": ["weekends", " weekends "],
            }
        )
        self.assertEqual(payload.sales_channels, ["walk_in", "whatsapp"])
        self.assertEqual(payload.peak_periods, ["weekends"])


class BusinessProfileV2ServiceTests(unittest.TestCase):
    def test_create_persists_lists_and_no_staleness(self) -> None:
        class FakeProfileRepo:
            def __init__(self) -> None:
                self.saved: BusinessProfileV2Read | None = None

            def get(self, _user_id: str) -> BusinessProfileV2Read | None:
                return None

            def create(self, profile: BusinessProfileV2Read) -> BusinessProfileV2Read:
                self.saved = profile
                return profile

        class FakeAnalysisRunRepo:
            def mark_stale_due_to_profile_change(self, _user_id: str) -> int:
                return 0

        profile_repo = FakeProfileRepo()
        service = BusinessProfileV2Service(
            profile_repository=profile_repo,
            analysis_run_repository=FakeAnalysisRunRepo(),
        )

        response = service.save_profile(sample_payload(), "user_123")

        self.assertEqual(response.analysis_impact.stale_analysis_runs, 0)
        self.assertEqual(profile_repo.saved.sales_channels, ["walk_in", "whatsapp", "referrals"])
        self.assertEqual(profile_repo.saved.peak_periods, ["holiday_periods", "weekends"])

    def test_updating_profile_marks_related_analysis_runs_stale(self) -> None:
        class FakeProfileRepo:
            def __init__(self) -> None:
                self.profile = sample_read_model()

            def get(self, _user_id: str) -> BusinessProfileV2Read:
                return self.profile

            def update(self, profile: BusinessProfileV2Read, _user_id: str) -> BusinessProfileV2Read:
                self.profile = profile
                return profile

        class FakeAnalysisRunRepo:
            def __init__(self) -> None:
                self.called = False

            def mark_stale_due_to_profile_change(self, _user_id: str) -> int:
                self.called = True
                return 2

        analysis_repo = FakeAnalysisRunRepo()
        service = BusinessProfileV2Service(
            profile_repository=FakeProfileRepo(),
            analysis_run_repository=analysis_repo,
        )

        response = service.save_profile(sample_payload(), "user_123")

        self.assertTrue(analysis_repo.called)
        self.assertTrue(response.analysis_impact.rerun_required)
        self.assertEqual(response.analysis_impact.stale_analysis_runs, 2)
        self.assertIn("rerun", response.analysis_impact.message or "")


class BusinessProfileV2RouteTests(unittest.TestCase):
    def setUp(self) -> None:
        self.app = FastAPI()
        self.app.include_router(business_profile_v2_router)
        self.app.dependency_overrides[get_current_user] = lambda: AuthenticatedUser(
            id="user_123",
            email="user@example.com",
        )
        self.client = TestClient(self.app)

    def tearDown(self) -> None:
        self.app.dependency_overrides.clear()

    def test_v2_route_requires_authentication(self) -> None:
        app_without_override = FastAPI()
        app_without_override.include_router(business_profile_v2_router)
        client = TestClient(app_without_override)

        response = client.get("/v2/business-profile")

        self.assertEqual(response.status_code, 401)

    def test_get_and_put_v2_business_profile(self) -> None:
        save_response = BusinessProfileV2SaveResponse(
            profile=sample_read_model(),
            analysis_impact={
                "stale_analysis_runs": 1,
                "rerun_required": True,
                "message": "Your business context changed. Future V2 analysis should be rerun to reflect the latest profile.",
            },
        )

        class FakeService:
            def get_profile(self, _user_id: str) -> BusinessProfileV2Read:
                return sample_read_model()

            def save_profile(self, _payload: BusinessProfileV2Create, _user_id: str) -> BusinessProfileV2SaveResponse:
                return save_response

        with patch("app.api.routes.routes_business_profile_v2.get_business_profile_v2_service", return_value=FakeService()):
            get_response = self.client.get("/v2/business-profile")
            put_response = self.client.put("/v2/business-profile", json=sample_payload().model_dump(by_alias=True))

        self.assertEqual(get_response.status_code, 200)
        self.assertEqual(get_response.json()["salesChannels"], ["walk_in", "whatsapp", "referrals"])
        self.assertEqual(put_response.status_code, 200)
        self.assertTrue(put_response.json()["analysisImpact"]["rerunRequired"])


if __name__ == "__main__":
    unittest.main()

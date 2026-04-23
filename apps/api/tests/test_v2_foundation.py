import unittest

from app.v2.config import (
    ACTION_FAMILY_REGISTRY,
    ADAPTIVE_MODULE_REGISTRY,
    BUSINESS_PROFILE_FIELD_REGISTRY,
    CORE_SECTION_REGISTRY,
    CRITICAL_RISK_TAXONOMY,
    ISSUE_TAXONOMY,
    SCALE_LIBRARY,
)
from app.v2.schemas.explainability import ExplainabilitySnapshot, ScoreDriver
from app.v2.schemas.interpretation import (
    InterpretationFallbackResult,
    TextInterpretationInput,
    TextInterpretationOutput,
)
from app.v2.schemas.lifecycle import (
    AIInterpretationStatus,
    AnalysisLifecycleState,
    FreshnessState,
    RerunReason,
    RerunRequirement,
)
from app.v2.schemas.meta import CURRENT_V2_VERSION_METADATA
from app.v2.schemas.snapshots import (
    AnalysisSnapshotEnvelope,
    AssessmentAnswerSnapshot,
    AssessmentSubmissionSnapshot,
    BusinessProfileSnapshot,
)


class V2FoundationTests(unittest.TestCase):
    def test_config_registry_validation(self) -> None:
        self.assertGreaterEqual(len(SCALE_LIBRARY), 5)
        self.assertGreaterEqual(len(BUSINESS_PROFILE_FIELD_REGISTRY), 15)
        self.assertEqual(len(CORE_SECTION_REGISTRY), 8)
        self.assertEqual(len(ADAPTIVE_MODULE_REGISTRY), 4)
        self.assertGreaterEqual(len(ISSUE_TAXONOMY), 5)
        self.assertGreaterEqual(len(CRITICAL_RISK_TAXONOMY), 2)
        self.assertGreaterEqual(len(ACTION_FAMILY_REGISTRY), 5)

    def test_version_metadata_defaults(self) -> None:
        dumped = CURRENT_V2_VERSION_METADATA.model_dump(by_alias=True)
        self.assertEqual(dumped["questionBankVersion"], "v2.0.0")
        self.assertEqual(dumped["analysisEngineVersion"], "v2.0.0-foundation")

    def test_lifecycle_model_behavior(self) -> None:
        state = AnalysisLifecycleState(
            freshness_status=FreshnessState.STALE_DUE_TO_ASSESSMENT_CHANGE,
            rerun_requirement=RerunRequirement.REQUIRED,
            rerun_required=True,
            rerun_reason=RerunReason.ASSESSMENT_CHANGED,
            ai_interpretation_status=AIInterpretationStatus.PARTIAL,
            usable_while_stale=True,
        )
        dumped = state.model_dump(mode="json", by_alias=True)
        self.assertEqual(dumped["freshnessStatus"], "stale_due_to_assessment_change")
        self.assertTrue(dumped["rerunRequired"])

    def test_snapshot_envelope_creation(self) -> None:
        snapshot = AnalysisSnapshotEnvelope(
            metadata=CURRENT_V2_VERSION_METADATA,
            lifecycle=AnalysisLifecycleState(
                freshness_status=FreshnessState.PROVISIONAL,
                ai_interpretation_status=AIInterpretationStatus.FALLBACK_USED,
            ),
            business_profile=BusinessProfileSnapshot(
                values={"industry": "retail", "size_band": "small", "team_size": 6}
            ),
            assessment_submission=AssessmentSubmissionSnapshot(
                sections=["operations"],
                answers=[
                    AssessmentAnswerSnapshot(
                        question_key="operations_process_documented",
                        section_key="operations",
                        answer_type="select",
                        value="partly_defined",
                    )
                ],
            ),
        )
        dumped = snapshot.model_dump(mode="json", by_alias=True)
        self.assertEqual(dumped["metadata"]["taxonomyVersion"], "v2.0.0")
        self.assertEqual(dumped["lifecycle"]["freshnessStatus"], "provisional")
        self.assertEqual(dumped["assessmentSubmission"]["answers"][0]["questionKey"], "operations_process_documented")

    def test_interpretation_and_explainability_serialization(self) -> None:
        interpretation = TextInterpretationOutput(
            question_key="growth_blocker_primary",
            section_key="growth_blockers",
            summary="The business is blocked by fragmented follow-up and weak visibility.",
            fallback=InterpretationFallbackResult(used=True, reason="provider_timeout", partial=True),
        )
        explainability = ExplainabilitySnapshot(
            score_drivers=[
                ScoreDriver(
                    code="OPS_PROCESS_GAP",
                    label="Process gap",
                    direction="down",
                    detail="Recurring work is not documented.",
                )
            ]
        )
        request = TextInterpretationInput(
            question_key="growth_blocker_primary",
            section_key="growth_blockers",
            answer_text="Manual coordination keeps slowing us down.",
            business_profile_context={"industry": "retail"},
        )

        self.assertTrue(interpretation.model_dump(by_alias=True)["fallback"]["used"])
        self.assertEqual(explainability.model_dump(by_alias=True)["scoreDrivers"][0]["code"], "OPS_PROCESS_GAP")
        self.assertEqual(request.model_dump(by_alias=True)["businessProfileContext"]["industry"], "retail")


if __name__ == "__main__":
    unittest.main()

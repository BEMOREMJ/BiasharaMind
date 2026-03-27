from datetime import UTC, datetime

from app.repositories.assessment_repository import assessment_repository
from app.schemas.assessment import (
    AssessmentCreate,
    AssessmentRead,
    AssessmentSubmit,
    AssessmentUpdate,
)


class AssessmentService:
    """Application service for the temporary assessment flow."""

    def get_assessment(self) -> AssessmentRead | None:
        return assessment_repository.get()

    def create_assessment(self, payload: AssessmentCreate) -> AssessmentRead:
        started_at = datetime.now(UTC).isoformat()
        assessment = AssessmentRead(
            id="assessment_v1",
            business_id="business_profile_v1",
            status="in_progress",
            version=payload.version,
            started_at=started_at,
            submitted_at=None,
            sections=payload.sections,
            answers=payload.answers,
        )
        return assessment_repository.create(assessment)

    def update_assessment(self, payload: AssessmentUpdate) -> AssessmentRead | None:
        existing = assessment_repository.get()
        if existing is None:
            return None

        updated = existing.model_copy(
            update={
                **payload.model_dump(exclude_none=True),
                "status": payload.status or "in_progress",
            }
        )
        return assessment_repository.update(updated)

    def submit_assessment(self, payload: AssessmentSubmit) -> AssessmentRead | None:
        existing = assessment_repository.get()
        if existing is None:
            return None

        submitted = existing.model_copy(
            update={
                "answers": payload.answers,
                "status": "submitted",
                "submitted_at": datetime.now(UTC).isoformat(),
            }
        )
        return assessment_repository.update(submitted)


assessment_service = AssessmentService()

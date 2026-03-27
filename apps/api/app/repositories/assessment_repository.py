from app.schemas.assessment import AssessmentRead


class InMemoryAssessmentRepository:
    """Temporary in-memory repository for the single active assessment V1 scaffold."""

    def __init__(self) -> None:
        self._assessment: AssessmentRead | None = None

    def get(self) -> AssessmentRead | None:
        if self._assessment is None:
            return None
        return self._assessment.model_copy(deep=True)

    def create(self, assessment: AssessmentRead) -> AssessmentRead:
        self._assessment = assessment.model_copy(deep=True)
        return self.get()

    def update(self, assessment: AssessmentRead) -> AssessmentRead:
        self._assessment = assessment.model_copy(deep=True)
        return self.get()


assessment_repository = InMemoryAssessmentRepository()

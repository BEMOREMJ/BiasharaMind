from app.schemas.analysis import AnalysisSummaryRead


class InMemoryAnalysisRepository:
    """Temporary in-memory repository for the single saved analysis summary."""

    def __init__(self) -> None:
        self._analysis: AnalysisSummaryRead | None = None

    def get(self) -> AnalysisSummaryRead | None:
        if self._analysis is None:
            return None
        return self._analysis.model_copy(deep=True)

    def save(self, analysis: AnalysisSummaryRead) -> AnalysisSummaryRead:
        self._analysis = analysis.model_copy(deep=True)
        return self.get()


analysis_repository = InMemoryAnalysisRepository()

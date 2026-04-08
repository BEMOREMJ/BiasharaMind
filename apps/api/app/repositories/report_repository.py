from app.schemas.report import ReportRead


class InMemoryReportRepository:
    """Temporary in-memory repository for the single generated report."""

    def __init__(self) -> None:
        self._report: ReportRead | None = None

    def get(self) -> ReportRead | None:
        if self._report is None:
            return None
        return self._report.model_copy(deep=True)

    def save(self, report: ReportRead) -> ReportRead:
        self._report = report.model_copy(deep=True)
        return self.get()


report_repository = InMemoryReportRepository()

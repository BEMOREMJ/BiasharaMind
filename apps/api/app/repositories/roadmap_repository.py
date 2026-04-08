from app.schemas.roadmap import RoadmapRead


class InMemoryRoadmapRepository:
    """Temporary in-memory repository for the single generated roadmap."""

    def __init__(self) -> None:
        self._roadmap: RoadmapRead | None = None

    def get(self) -> RoadmapRead | None:
        if self._roadmap is None:
            return None
        return self._roadmap.model_copy(deep=True)

    def save(self, roadmap: RoadmapRead) -> RoadmapRead:
        self._roadmap = roadmap.model_copy(deep=True)
        return self.get()


roadmap_repository = InMemoryRoadmapRepository()

from app.schemas.business_profile import BusinessProfileRead


class InMemoryBusinessProfileRepository:
    """Temporary in-memory repository for the single-profile V1 scaffold."""

    def __init__(self) -> None:
        self._profile: BusinessProfileRead | None = None

    def get(self) -> BusinessProfileRead | None:
        if self._profile is None:
            return None
        return self._profile.model_copy(deep=True)

    def create(self, profile: BusinessProfileRead) -> BusinessProfileRead:
        self._profile = profile.model_copy(deep=True)
        return self.get()

    def update(self, profile: BusinessProfileRead) -> BusinessProfileRead:
        self._profile = profile.model_copy(deep=True)
        return self.get()


business_profile_repository = InMemoryBusinessProfileRepository()

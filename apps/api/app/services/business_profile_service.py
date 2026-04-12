from datetime import UTC, datetime
from uuid import uuid4

from app.repositories.business_profile_repository import business_profile_repository
from app.schemas.business_profile import (
    BusinessProfileCreate,
    BusinessProfileRead,
    BusinessProfileUpdate,
)


class BusinessProfileService:
    """Application service for the temporary business profile feature slice."""

    def get_profile(self) -> BusinessProfileRead | None:
        return business_profile_repository.get()

    def create_profile(self, payload: BusinessProfileCreate) -> BusinessProfileRead:
        timestamp = datetime.now(UTC).isoformat()
        profile = BusinessProfileRead(
            id=f"business_profile_{uuid4().hex}",
            user_id="demo_user_v1",
            created_at=timestamp,
            updated_at=timestamp,
            **payload.model_dump(),
        )
        return business_profile_repository.create(profile)

    def update_profile(self, payload: BusinessProfileUpdate) -> BusinessProfileRead | None:
        existing = business_profile_repository.get()
        if existing is None:
            return None

        updated = existing.model_copy(
            update={
                **payload.model_dump(exclude_none=True),
                "updated_at": datetime.now(UTC).isoformat(),
            }
        )
        return business_profile_repository.update(updated)


business_profile_service = BusinessProfileService()

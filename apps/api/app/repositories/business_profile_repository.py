from sqlalchemy import select

from app.db.session import session_scope
from app.models.business_profile import BusinessProfileRecord
from app.schemas.business_profile import BusinessProfileRead


def _to_schema(record: BusinessProfileRecord) -> BusinessProfileRead:
    return BusinessProfileRead(
        id=record.id,
        user_id=record.user_id or "demo_user_v1",
        created_at=record.created_at.isoformat(),
        updated_at=record.updated_at.isoformat(),
        business_name=record.business_name,
        industry=record.industry,
        country=record.country,
        size_band=record.size_band,
        years_operating=record.years_operating,
        revenue_band=record.revenue_band,
        team_size=record.team_size,
        main_goal=record.main_goal,
        budget_band=record.budget_band,
        current_tools=list(record.current_tools or []),
    )


class BusinessProfileRepository:
    """PostgreSQL-backed repository for the single active business profile."""

    def get(self) -> BusinessProfileRead | None:
        with session_scope() as session:
            record = session.scalar(
                select(BusinessProfileRecord)
                .where(BusinessProfileRecord.is_active.is_(True))
                .order_by(BusinessProfileRecord.updated_at.desc())
                .limit(1)
            )
            if record is None:
                return None
            return _to_schema(record)

    def create(self, profile: BusinessProfileRead) -> BusinessProfileRead:
        with session_scope() as session:
            record = BusinessProfileRecord(
                id=profile.id,
                user_id=profile.user_id,
                business_name=profile.business_name,
                industry=profile.industry,
                country=profile.country,
                size_band=profile.size_band,
                years_operating=profile.years_operating,
                revenue_band=profile.revenue_band,
                team_size=profile.team_size,
                main_goal=profile.main_goal,
                budget_band=profile.budget_band,
                current_tools=profile.current_tools,
            )
            session.add(record)
            session.flush()
            session.refresh(record)
            return _to_schema(record)

    def update(self, profile: BusinessProfileRead) -> BusinessProfileRead:
        with session_scope() as session:
            record = session.get(BusinessProfileRecord, profile.id)
            if record is None:
                raise ValueError(f"Business profile {profile.id} not found")

            record.user_id = profile.user_id
            record.business_name = profile.business_name
            record.industry = profile.industry
            record.country = profile.country
            record.size_band = profile.size_band
            record.years_operating = profile.years_operating
            record.revenue_band = profile.revenue_band
            record.team_size = profile.team_size
            record.main_goal = profile.main_goal
            record.budget_band = profile.budget_band
            record.current_tools = profile.current_tools
            session.flush()
            session.refresh(record)
            return _to_schema(record)


business_profile_repository = BusinessProfileRepository()

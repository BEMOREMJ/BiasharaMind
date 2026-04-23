from sqlalchemy import select

from app.db.session import session_scope
from app.models.business_profile_v2 import BusinessProfileV2Record
from app.v2.schemas.profile import BusinessProfileV2Read, ImprovementCapacityPayload


def _to_schema(record: BusinessProfileV2Record) -> BusinessProfileV2Read:
    return BusinessProfileV2Read(
        id=record.id,
        user_id=record.user_id or "demo_user_v2",
        created_at=record.created_at.isoformat(),
        updated_at=record.updated_at.isoformat(),
        business_name=record.business_name,
        primary_business_type=record.primary_business_type,
        main_offer=record.main_offer,
        customer_type=record.customer_type,
        sales_channels=list(record.sales_channels or []),
        fulfilment_model=record.fulfilment_model,
        inventory_involvement=record.inventory_involvement,
        credit_sales_exposure=record.credit_sales_exposure,
        business_age_stage=record.business_age_stage,
        team_size_band=record.team_size_band,
        number_of_locations=record.number_of_locations,
        monthly_revenue_band=record.monthly_revenue_band,
        seasonality_level=record.seasonality_level,
        peak_periods=list(record.peak_periods or []) or None,
        owner_involvement_level=record.owner_involvement_level,
        primary_business_goal=record.primary_business_goal,
        improvement_capacity=ImprovementCapacityPayload(
            time_capacity=record.time_capacity,
            budget_flexibility=record.budget_flexibility,
            tool_hire_openness=record.tool_hire_openness,
        ),
        record_availability=record.record_availability,
        compliance_sector_sensitivity=record.compliance_sector_sensitivity,
    )


class BusinessProfileV2Repository:
    def get(self, user_id: str) -> BusinessProfileV2Read | None:
        with session_scope() as session:
            record = session.scalar(
                select(BusinessProfileV2Record)
                .where(BusinessProfileV2Record.user_id == user_id)
                .order_by(BusinessProfileV2Record.updated_at.desc())
                .limit(1)
            )
            if record is None:
                return None
            return _to_schema(record)

    def get_by_id(self, profile_id: str, user_id: str) -> BusinessProfileV2Read | None:
        with session_scope() as session:
            record = session.scalar(
                select(BusinessProfileV2Record)
                .where(BusinessProfileV2Record.id == profile_id)
                .where(BusinessProfileV2Record.user_id == user_id)
                .limit(1)
            )
            if record is None:
                return None
            return _to_schema(record)

    def create(self, profile: BusinessProfileV2Read) -> BusinessProfileV2Read:
        with session_scope() as session:
            record = BusinessProfileV2Record(
                id=profile.id,
                user_id=profile.user_id,
                business_name=profile.business_name,
                primary_business_type=profile.primary_business_type,
                main_offer=profile.main_offer,
                customer_type=profile.customer_type,
                sales_channels=profile.sales_channels,
                fulfilment_model=profile.fulfilment_model,
                inventory_involvement=profile.inventory_involvement,
                credit_sales_exposure=profile.credit_sales_exposure,
                business_age_stage=profile.business_age_stage,
                team_size_band=profile.team_size_band,
                number_of_locations=profile.number_of_locations,
                monthly_revenue_band=profile.monthly_revenue_band,
                seasonality_level=profile.seasonality_level,
                peak_periods=profile.peak_periods,
                owner_involvement_level=profile.owner_involvement_level,
                primary_business_goal=profile.primary_business_goal,
                time_capacity=profile.improvement_capacity.time_capacity,
                budget_flexibility=profile.improvement_capacity.budget_flexibility,
                tool_hire_openness=profile.improvement_capacity.tool_hire_openness,
                record_availability=profile.record_availability,
                compliance_sector_sensitivity=profile.compliance_sector_sensitivity,
            )
            session.add(record)
            session.flush()
            session.refresh(record)
            return _to_schema(record)

    def update(self, profile: BusinessProfileV2Read, user_id: str) -> BusinessProfileV2Read:
        with session_scope() as session:
            record = session.scalar(
                select(BusinessProfileV2Record)
                .where(BusinessProfileV2Record.id == profile.id)
                .where(BusinessProfileV2Record.user_id == user_id)
                .limit(1)
            )
            if record is None:
                raise ValueError(f"Business profile v2 {profile.id} not found")

            record.business_name = profile.business_name
            record.primary_business_type = profile.primary_business_type
            record.main_offer = profile.main_offer
            record.customer_type = profile.customer_type
            record.sales_channels = profile.sales_channels
            record.fulfilment_model = profile.fulfilment_model
            record.inventory_involvement = profile.inventory_involvement
            record.credit_sales_exposure = profile.credit_sales_exposure
            record.business_age_stage = profile.business_age_stage
            record.team_size_band = profile.team_size_band
            record.number_of_locations = profile.number_of_locations
            record.monthly_revenue_band = profile.monthly_revenue_band
            record.seasonality_level = profile.seasonality_level
            record.peak_periods = profile.peak_periods
            record.owner_involvement_level = profile.owner_involvement_level
            record.primary_business_goal = profile.primary_business_goal
            record.time_capacity = profile.improvement_capacity.time_capacity
            record.budget_flexibility = profile.improvement_capacity.budget_flexibility
            record.tool_hire_openness = profile.improvement_capacity.tool_hire_openness
            record.record_availability = profile.record_availability
            record.compliance_sector_sensitivity = profile.compliance_sector_sensitivity
            session.flush()
            session.refresh(record)
            return _to_schema(record)


business_profile_v2_repository = BusinessProfileV2Repository()

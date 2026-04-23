from datetime import UTC, datetime
from typing import Any
from uuid import uuid4

from pydantic import Field, field_validator, model_validator

from app.v2.common import V2BaseModel
from app.v2.config.profile import BUSINESS_PROFILE_FIELD_MAP, get_profile_enum_values


def _validate_enum_value(field_key: str, value: str | None) -> str | None:
    if value is None:
        return None
    allowed_values = get_profile_enum_values(field_key)
    if allowed_values and value not in allowed_values:
        raise ValueError(f"{field_key} must be one of: {', '.join(sorted(allowed_values))}")
    return value


def _normalize_multi_enum(field_key: str, value: list[str] | None) -> list[str] | None:
    if value is None:
        return None
    cleaned: list[str] = []
    allowed_values = get_profile_enum_values(field_key)
    for item in value:
        normalized = item.strip()
        if not normalized:
            continue
        if allowed_values and normalized not in allowed_values:
            raise ValueError(f"{field_key} must only contain supported values")
        if normalized not in cleaned:
            cleaned.append(normalized)
    return cleaned


class ImprovementCapacityPayload(V2BaseModel):
    time_capacity: str
    budget_flexibility: str
    tool_hire_openness: str

    @field_validator("time_capacity")
    @classmethod
    def validate_time_capacity(cls, value: str) -> str:
        return _validate_enum_value("time_capacity", value) or value

    @field_validator("budget_flexibility")
    @classmethod
    def validate_budget_flexibility(cls, value: str) -> str:
        return _validate_enum_value("budget_flexibility", value) or value

    @field_validator("tool_hire_openness")
    @classmethod
    def validate_tool_hire_openness(cls, value: str) -> str:
        return _validate_enum_value("tool_hire_openness", value) or value


class BusinessProfileV2Base(V2BaseModel):
    business_name: str = Field(min_length=1, max_length=120)
    primary_business_type: str = Field(min_length=1, max_length=64)
    main_offer: str = Field(min_length=1, max_length=240)
    customer_type: str = Field(min_length=1, max_length=64)
    sales_channels: list[str] = Field(min_length=1, max_length=8)
    fulfilment_model: str = Field(min_length=1, max_length=64)
    inventory_involvement: str = Field(min_length=1, max_length=64)
    credit_sales_exposure: str = Field(min_length=1, max_length=64)
    business_age_stage: str = Field(min_length=1, max_length=64)
    team_size_band: str = Field(min_length=1, max_length=64)
    number_of_locations: int = Field(ge=1, le=500)
    monthly_revenue_band: str = Field(min_length=1, max_length=64)
    seasonality_level: str | None = Field(default=None, max_length=64)
    peak_periods: list[str] | None = Field(default=None, max_length=8)
    owner_involvement_level: str = Field(min_length=1, max_length=64)
    primary_business_goal: str = Field(min_length=1, max_length=64)
    improvement_capacity: ImprovementCapacityPayload
    record_availability: str = Field(min_length=1, max_length=64)
    compliance_sector_sensitivity: str | None = Field(default=None, max_length=64)

    @field_validator(
        "primary_business_type",
        "customer_type",
        "fulfilment_model",
        "inventory_involvement",
        "credit_sales_exposure",
        "business_age_stage",
        "team_size_band",
        "monthly_revenue_band",
        "seasonality_level",
        "owner_involvement_level",
        "primary_business_goal",
        "record_availability",
        "compliance_sector_sensitivity",
    )
    @classmethod
    def validate_registry_enum_fields(cls, value: str | None, info: Any) -> str | None:
        return _validate_enum_value(info.field_name, value)

    @field_validator("sales_channels")
    @classmethod
    def validate_sales_channels(cls, value: list[str]) -> list[str]:
        normalized = _normalize_multi_enum("sales_channels", value) or []
        if not normalized:
            raise ValueError("sales_channels must include at least one selection")
        return normalized

    @field_validator("peak_periods")
    @classmethod
    def validate_peak_periods(cls, value: list[str] | None) -> list[str] | None:
        normalized = _normalize_multi_enum("peak_periods", value)
        return normalized or None

    @model_validator(mode="after")
    def validate_optional_dependencies(self) -> "BusinessProfileV2Base":
        if self.peak_periods and not self.seasonality_level:
            raise ValueError("seasonality_level is required when peak_periods are provided")
        return self


class BusinessProfileV2Create(BusinessProfileV2Base):
    pass


class BusinessProfileV2Update(BusinessProfileV2Base):
    pass


class BusinessProfileV2Read(BusinessProfileV2Base):
    id: str
    user_id: str
    created_at: str
    updated_at: str


class AnalysisImpactSummary(V2BaseModel):
    stale_analysis_runs: int = Field(ge=0, default=0)
    rerun_required: bool = False
    message: str | None = Field(default=None, max_length=240)


class BusinessProfileV2SaveResponse(V2BaseModel):
    profile: BusinessProfileV2Read
    analysis_impact: AnalysisImpactSummary


def create_business_profile_v2_read(payload: BusinessProfileV2Create, user_id: str) -> BusinessProfileV2Read:
    timestamp = datetime.now(UTC).isoformat()
    return BusinessProfileV2Read(
        id=f"business_profile_v2_{uuid4().hex}",
        user_id=user_id,
        created_at=timestamp,
        updated_at=timestamp,
        **payload.model_dump(),
    )


def apply_business_profile_v2_update(
    existing: BusinessProfileV2Read,
    payload: BusinessProfileV2Update,
) -> BusinessProfileV2Read:
    return existing.model_copy(
        update={
            **payload.model_dump(),
            "updated_at": datetime.now(UTC).isoformat(),
        }
    )

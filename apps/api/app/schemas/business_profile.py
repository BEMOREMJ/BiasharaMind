from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator


def to_camel(value: str) -> str:
    head, *tail = value.split("_")
    return head + "".join(segment.capitalize() for segment in tail)


Industry = Literal[
    "retail",
    "hospitality",
    "services",
    "manufacturing",
    "agriculture",
    "healthcare",
    "education",
    "technology",
    "construction",
    "logistics",
    "other",
]

BusinessSizeBand = Literal["solo", "micro", "small", "medium"]
RevenueBand = Literal[
    "pre_revenue",
    "under_10k_usd",
    "10k_to_50k_usd",
    "50k_to_250k_usd",
    "250k_to_1m_usd",
    "over_1m_usd",
]
BudgetBand = Literal[
    "none",
    "under_500_usd_per_month",
    "500_to_2000_usd_per_month",
    "2000_to_10000_usd_per_month",
    "over_10000_usd_per_month",
]


class BusinessProfileBase(BaseModel):
    business_name: str = Field(min_length=1, max_length=120)
    industry: Industry
    country: str = Field(min_length=2, max_length=2)
    size_band: BusinessSizeBand
    years_operating: int = Field(ge=0, le=100)
    revenue_band: RevenueBand
    team_size: int = Field(ge=1, le=10000)
    main_goal: str = Field(min_length=1, max_length=240)
    budget_band: BudgetBand
    current_tools: list[str] = Field(default_factory=list, max_length=20)

    model_config = ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True,
        str_strip_whitespace=True,
    )

    @field_validator("country")
    @classmethod
    def validate_country(cls, value: str) -> str:
        normalized = value.upper()
        if len(normalized) != 2 or not normalized.isalpha():
            raise ValueError("country must be a 2-letter uppercase code")
        return normalized

    @field_validator("current_tools")
    @classmethod
    def validate_tools(cls, value: list[str]) -> list[str]:
        cleaned = [tool.strip() for tool in value if tool.strip()]
        if len(cleaned) > 20:
            raise ValueError("current_tools cannot contain more than 20 items")
        return cleaned


class BusinessProfileCreate(BusinessProfileBase):
    pass


class BusinessProfileUpdate(BaseModel):
    business_name: str | None = Field(default=None, min_length=1, max_length=120)
    industry: Industry | None = None
    country: str | None = Field(default=None, min_length=2, max_length=2)
    size_band: BusinessSizeBand | None = None
    years_operating: int | None = Field(default=None, ge=0, le=100)
    revenue_band: RevenueBand | None = None
    team_size: int | None = Field(default=None, ge=1, le=10000)
    main_goal: str | None = Field(default=None, min_length=1, max_length=240)
    budget_band: BudgetBand | None = None
    current_tools: list[str] | None = Field(default=None, max_length=20)

    model_config = ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True,
        str_strip_whitespace=True,
    )

    @field_validator("country")
    @classmethod
    def validate_country(cls, value: str | None) -> str | None:
        if value is None:
            return value
        normalized = value.upper()
        if len(normalized) != 2 or not normalized.isalpha():
            raise ValueError("country must be a 2-letter uppercase code")
        return normalized

    @field_validator("current_tools")
    @classmethod
    def validate_tools(cls, value: list[str] | None) -> list[str] | None:
        if value is None:
            return value
        cleaned = [tool.strip() for tool in value if tool.strip()]
        if len(cleaned) > 20:
            raise ValueError("current_tools cannot contain more than 20 items")
        return cleaned

    @model_validator(mode="after")
    def validate_has_updates(self) -> "BusinessProfileUpdate":
        if not self.model_dump(exclude_none=True):
            raise ValueError("At least one field must be provided")
        return self


class BusinessProfileRead(BusinessProfileBase):
    id: str
    user_id: str
    created_at: str
    updated_at: str

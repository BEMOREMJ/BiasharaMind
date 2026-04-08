from pydantic import BaseModel, ConfigDict, Field

from app.schemas.business_profile import to_camel


class RoadmapAction(BaseModel):
    title: str = Field(min_length=1, max_length=140)
    description: str = Field(min_length=1, max_length=400)
    why_it_matters: str = Field(min_length=1, max_length=240)
    effort: str = Field(min_length=1, max_length=20)
    cost_band: str = Field(min_length=1, max_length=20)
    expected_impact: str = Field(min_length=1, max_length=20)

    model_config = ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True,
        str_strip_whitespace=True,
    )


class RoadmapRead(BaseModel):
    id: str
    analysis_id: str
    days0to30: list[RoadmapAction] = Field(default_factory=list, max_length=10)
    days31to60: list[RoadmapAction] = Field(default_factory=list, max_length=10)
    days61to90: list[RoadmapAction] = Field(default_factory=list, max_length=10)
    created_at: str

    model_config = ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True,
        str_strip_whitespace=True,
    )

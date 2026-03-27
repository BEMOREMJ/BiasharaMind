from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

from app.schemas.business_profile import to_camel

EffortLevel = Literal["low", "medium", "high"]
CostBand = Literal["low", "medium", "high"]
ExpectedImpact = Literal["low", "medium", "high"]


class AnalysisCategoryScore(BaseModel):
    section_key: str = Field(min_length=2, max_length=64)
    label: str = Field(min_length=1, max_length=120)
    score: float = Field(ge=0, le=100)

    model_config = ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True,
        str_strip_whitespace=True,
    )


class PriorityRecommendation(BaseModel):
    title: str = Field(min_length=1, max_length=140)
    why: str = Field(min_length=1, max_length=400)
    effort: EffortLevel
    cost_band: CostBand
    expected_impact: ExpectedImpact

    model_config = ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True,
        str_strip_whitespace=True,
    )


class AnalysisSummaryRead(BaseModel):
    id: str
    assessment_id: str
    overall_score: float = Field(ge=0, le=100)
    category_scores: list[AnalysisCategoryScore] = Field(min_length=1, max_length=12)
    top_strengths: list[str] = Field(min_length=1, max_length=5)
    top_risks: list[str] = Field(min_length=1, max_length=5)
    top_priorities: list[PriorityRecommendation] = Field(min_length=1, max_length=5)
    created_at: str
    model_version: str = Field(min_length=1, max_length=64)
    workflow_version: str = Field(min_length=1, max_length=64)

    model_config = ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True,
        str_strip_whitespace=True,
    )

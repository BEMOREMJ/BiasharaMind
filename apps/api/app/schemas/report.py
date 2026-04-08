from pydantic import BaseModel, ConfigDict, Field

from app.schemas.analysis import AnalysisCategoryScore, PriorityRecommendation
from app.schemas.business_profile import to_camel
from app.schemas.roadmap import RoadmapAction


class ReportBusinessSummary(BaseModel):
    business_name: str = Field(min_length=1, max_length=120)
    industry: str = Field(min_length=1, max_length=80)
    country: str = Field(min_length=2, max_length=2)
    size_band: str = Field(min_length=1, max_length=40)
    team_size: int = Field(ge=1, le=10000)
    main_goal: str = Field(min_length=1, max_length=240)

    model_config = ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True,
        str_strip_whitespace=True,
    )


class ReportRoadmapPhase(BaseModel):
    label: str = Field(min_length=1, max_length=40)
    actions: list[RoadmapAction] = Field(default_factory=list, max_length=10)

    model_config = ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True,
        str_strip_whitespace=True,
    )


class ReportRead(BaseModel):
    id: str
    analysis_id: str
    format: str = Field(min_length=1, max_length=20)
    storage_path: str = Field(min_length=1, max_length=240)
    created_at: str
    business_summary: ReportBusinessSummary
    overall_score: float = Field(ge=0, le=100)
    category_scores: list[AnalysisCategoryScore] = Field(min_length=1, max_length=12)
    strengths: list[str] = Field(min_length=1, max_length=5)
    risks: list[str] = Field(min_length=1, max_length=5)
    priorities: list[PriorityRecommendation] = Field(min_length=1, max_length=5)
    roadmap_phases: list[ReportRoadmapPhase] = Field(min_length=1, max_length=3)
    export_file_name: str = Field(min_length=1, max_length=120)

    model_config = ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True,
        str_strip_whitespace=True,
    )

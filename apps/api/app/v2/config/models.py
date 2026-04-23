from typing import Literal

from pydantic import Field, model_validator

from app.v2.common import V2BaseModel

QuestionInputType = Literal["select", "number", "text", "textarea", "multiselect"]
ModuleTriggerType = Literal["profile_field"]
TaxonomySeverity = Literal["low", "medium", "high", "critical"]
ActionHorizon = Literal["now", "next", "later"]


class ScaleOption(V2BaseModel):
    value: str = Field(min_length=1, max_length=64)
    label: str = Field(min_length=1, max_length=120)
    numeric_value: float = Field(ge=0, le=100)
    evidence_hint: str | None = Field(default=None, max_length=240)


class ScaleDefinition(V2BaseModel):
    key: str = Field(min_length=2, max_length=64, pattern=r"^[a-z0-9_]+$")
    label: str = Field(min_length=1, max_length=120)
    response_type: Literal["single_select", "numeric", "free_text"]
    options: list[ScaleOption] = Field(default_factory=list, max_length=10)
    min_value: float | None = Field(default=None, ge=0, le=100)
    max_value: float | None = Field(default=None, ge=0, le=100)
    step: float | None = Field(default=None, gt=0, le=100)

    @model_validator(mode="after")
    def validate_shape(self) -> "ScaleDefinition":
        if self.response_type == "single_select" and not self.options:
            raise ValueError("single_select scales require options")
        if self.response_type != "single_select" and self.options:
            raise ValueError("only single_select scales may define options")
        if self.response_type == "numeric" and (self.min_value is None or self.max_value is None):
            raise ValueError("numeric scales require min_value and max_value")
        return self


class BusinessProfileEnumOption(V2BaseModel):
    value: str = Field(min_length=1, max_length=64)
    label: str = Field(min_length=1, max_length=120)
    description: str | None = Field(default=None, max_length=240)


class BusinessProfileFieldDefinition(V2BaseModel):
    key: str = Field(min_length=2, max_length=64, pattern=r"^[a-z0-9_]+$")
    label: str = Field(min_length=1, max_length=120)
    field_type: Literal["enum", "multi_enum", "number", "string", "country_code"]
    required: bool = True
    description: str | None = Field(default=None, max_length=280)
    options: list[BusinessProfileEnumOption] = Field(default_factory=list, max_length=20)
    min_value: int | None = Field(default=None, ge=0)
    max_value: int | None = Field(default=None, ge=0)
    routing_relevant: bool = True

    @model_validator(mode="after")
    def validate_shape(self) -> "BusinessProfileFieldDefinition":
        if self.field_type in {"enum", "multi_enum"} and not self.options:
            raise ValueError("enum profile fields require options")
        if self.field_type not in {"enum", "multi_enum"} and self.options:
            raise ValueError("non-enum profile fields cannot define options")
        return self


class QuestionDefinition(V2BaseModel):
    key: str = Field(min_length=2, max_length=64, pattern=r"^[a-z0-9_]+$")
    prompt: str = Field(min_length=1, max_length=320)
    input_type: QuestionInputType
    required: bool = True
    scale_key: str | None = Field(default=None, min_length=2, max_length=64)
    help_text: str | None = Field(default=None, max_length=240)
    interpretation_enabled: bool = False
    tags: list[str] = Field(default_factory=list, max_length=10)
    essential: bool = False
    scored: bool = True
    bucket: str = Field(min_length=1, max_length=64)
    allow_unknown: bool = False
    allow_prefer_not_to_say: bool = False
    max_length: int | None = Field(default=None, ge=1, le=4000)
    multi_select_max_items: int | None = Field(default=None, ge=1, le=12)


class SectionDefinition(V2BaseModel):
    key: str = Field(min_length=2, max_length=64, pattern=r"^[a-z0-9_]+$")
    label: str = Field(min_length=1, max_length=120)
    description: str = Field(min_length=1, max_length=280)
    order: int = Field(ge=1, le=20)
    questions: list[QuestionDefinition] = Field(min_length=1, max_length=20)


class AdaptiveModuleDefinition(V2BaseModel):
    key: str = Field(min_length=2, max_length=64, pattern=r"^[a-z0-9_]+$")
    label: str = Field(min_length=1, max_length=120)
    description: str = Field(min_length=1, max_length=280)
    trigger_type: ModuleTriggerType
    trigger_field: str = Field(min_length=2, max_length=64)
    trigger_values: list[str] = Field(min_length=1, max_length=20)
    parent_section_key: str = Field(min_length=2, max_length=64)
    questions: list[QuestionDefinition] = Field(min_length=1, max_length=12)


class IssueTaxonomyEntry(V2BaseModel):
    code: str = Field(min_length=2, max_length=64, pattern=r"^[A-Z0-9_]+$")
    label: str = Field(min_length=1, max_length=140)
    description: str = Field(min_length=1, max_length=320)
    section_key: str = Field(min_length=2, max_length=64)
    severity: TaxonomySeverity
    action_family_codes: list[str] = Field(default_factory=list, max_length=6)


class CriticalRiskTaxonomyEntry(V2BaseModel):
    code: str = Field(min_length=2, max_length=64, pattern=r"^[A-Z0-9_]+$")
    label: str = Field(min_length=1, max_length=140)
    description: str = Field(min_length=1, max_length=320)
    severity: Literal["critical"]
    issue_codes: list[str] = Field(default_factory=list, max_length=10)
    action_family_codes: list[str] = Field(default_factory=list, max_length=6)


class ActionFamilyEntry(V2BaseModel):
    code: str = Field(min_length=2, max_length=64, pattern=r"^[A-Z0-9_]+$")
    label: str = Field(min_length=1, max_length=140)
    description: str = Field(min_length=1, max_length=320)
    default_horizon: ActionHorizon
    issue_codes: list[str] = Field(default_factory=list, max_length=20)
    critical_risk_codes: list[str] = Field(default_factory=list, max_length=20)

from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, model_validator

from app.schemas.business_profile import to_camel

AssessmentStatus = Literal["not_started", "in_progress", "submitted", "analyzed"]
AssessmentAnswerType = Literal["text", "number", "select", "textarea"]


class AssessmentSection(BaseModel):
    key: str = Field(min_length=2, max_length=64)
    title: str = Field(min_length=1, max_length=120)
    description: str = Field(min_length=1, max_length=280)
    order: int = Field(ge=1, le=50)

    model_config = ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True,
        str_strip_whitespace=True,
    )


class AssessmentAnswer(BaseModel):
    question_key: str = Field(min_length=2, max_length=64)
    section_key: str = Field(min_length=2, max_length=64)
    answer_type: AssessmentAnswerType
    value: str | float | int

    model_config = ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True,
        str_strip_whitespace=True,
    )

    @model_validator(mode="after")
    def validate_value(self) -> "AssessmentAnswer":
        if self.answer_type == "number" and not isinstance(self.value, (int, float)):
            raise ValueError("number answers must use a numeric value")

        if self.answer_type in {"text", "textarea", "select"} and not isinstance(self.value, str):
            raise ValueError("text, textarea, and select answers must use a string value")

        return self


class AssessmentCreate(BaseModel):
    version: str = Field(min_length=1, max_length=32)
    sections: list[AssessmentSection] = Field(min_length=1, max_length=12)
    answers: list[AssessmentAnswer] = Field(default_factory=list, max_length=100)

    model_config = ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True,
        str_strip_whitespace=True,
    )


class AssessmentUpdate(BaseModel):
    status: AssessmentStatus | None = None
    sections: list[AssessmentSection] | None = Field(default=None, min_length=1, max_length=12)
    answers: list[AssessmentAnswer] | None = Field(default=None, max_length=100)

    model_config = ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True,
        str_strip_whitespace=True,
    )

    @model_validator(mode="after")
    def validate_has_updates(self) -> "AssessmentUpdate":
        if not self.model_dump(exclude_none=True):
            raise ValueError("At least one field must be provided")
        return self


class AssessmentSubmit(BaseModel):
    answers: list[AssessmentAnswer] = Field(default_factory=list, max_length=100)

    model_config = ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True,
        str_strip_whitespace=True,
    )


class AssessmentRead(BaseModel):
    id: str
    business_id: str
    status: AssessmentStatus
    version: str = Field(min_length=1, max_length=32)
    started_at: str
    submitted_at: str | None = None
    sections: list[AssessmentSection] = Field(min_length=1, max_length=12)
    answers: list[AssessmentAnswer] = Field(default_factory=list, max_length=100)

    model_config = ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True,
        str_strip_whitespace=True,
    )

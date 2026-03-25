from typing import Any, TypedDict


class AssessmentWorkflowState(TypedDict, total=False):
    business_profile: dict[str, Any]
    assessment_answers: list[dict[str, Any]]
    retrieved_context: list[dict[str, Any]]
    scores: dict[str, Any]
    insights: dict[str, Any]
    priorities: list[dict[str, Any]]
    roadmap: dict[str, Any]
    persisted: bool
    errors: list[str]

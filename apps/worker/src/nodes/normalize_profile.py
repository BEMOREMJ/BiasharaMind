from src.state.assessment_state import AssessmentWorkflowState


def normalize_profile(state: AssessmentWorkflowState) -> AssessmentWorkflowState:
    profile = dict(state.get("business_profile", {}))
    normalized_name = str(profile.get("business_name", "")).strip()

    if normalized_name:
        profile["business_name"] = normalized_name

    return {"business_profile": profile}

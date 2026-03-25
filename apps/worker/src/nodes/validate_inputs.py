from src.state.assessment_state import AssessmentWorkflowState


def validate_inputs(state: AssessmentWorkflowState) -> AssessmentWorkflowState:
    errors = list(state.get("errors", []))

    if not state.get("business_profile"):
        errors.append("Missing business_profile")

    if not state.get("assessment_answers"):
        errors.append("Missing assessment_answers")

    return {"errors": errors}

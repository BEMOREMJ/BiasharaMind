from src.state.assessment_state import AssessmentWorkflowState


def persist_results(state: AssessmentWorkflowState) -> AssessmentWorkflowState:
    has_errors = bool(state.get("errors"))
    return {"persisted": not has_errors}

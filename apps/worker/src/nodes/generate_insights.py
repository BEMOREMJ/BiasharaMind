from src.state.assessment_state import AssessmentWorkflowState


def generate_insights(state: AssessmentWorkflowState) -> AssessmentWorkflowState:
    score_summary = state.get("scores", {})
    return {
        "insights": {
            "summary": "Placeholder insights generated from scaffolded workflow state.",
            "score_context": score_summary,
        }
    }

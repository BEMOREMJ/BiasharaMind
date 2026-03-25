from src.state.assessment_state import AssessmentWorkflowState


def score_assessment(state: AssessmentWorkflowState) -> AssessmentWorkflowState:
    answer_count = len(state.get("assessment_answers", []))
    return {
        "scores": {
            "overall": 0,
            "answered_questions": answer_count,
            "status": "placeholder",
        }
    }

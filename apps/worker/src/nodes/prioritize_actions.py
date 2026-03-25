from src.state.assessment_state import AssessmentWorkflowState


def prioritize_actions(state: AssessmentWorkflowState) -> AssessmentWorkflowState:
    return {
        "priorities": [
            {
                "title": "Define top priorities",
                "why": "Placeholder recommendation until prioritization logic is implemented.",
                "source": "scaffold",
            }
        ]
    }

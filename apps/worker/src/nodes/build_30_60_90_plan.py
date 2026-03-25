from src.state.assessment_state import AssessmentWorkflowState


def build_30_60_90_plan(state: AssessmentWorkflowState) -> AssessmentWorkflowState:
    priorities = state.get("priorities", [])
    return {
        "roadmap": {
            "days0to30": priorities[:1],
            "days31to60": [],
            "days61to90": [],
        }
    }

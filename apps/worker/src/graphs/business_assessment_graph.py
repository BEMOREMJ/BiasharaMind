from langgraph.graph import END, START, StateGraph

from src.nodes.build_30_60_90_plan import build_30_60_90_plan
from src.nodes.generate_insights import generate_insights
from src.nodes.normalize_profile import normalize_profile
from src.nodes.persist_results import persist_results
from src.nodes.prioritize_actions import prioritize_actions
from src.nodes.retrieve_knowledge import retrieve_knowledge
from src.nodes.score_assessment import score_assessment
from src.nodes.validate_inputs import validate_inputs
from src.state.assessment_state import AssessmentWorkflowState


def build_business_assessment_graph():
    graph = StateGraph(AssessmentWorkflowState)

    graph.add_node("validate_inputs", validate_inputs)
    graph.add_node("normalize_profile", normalize_profile)
    graph.add_node("retrieve_knowledge", retrieve_knowledge)
    graph.add_node("score_assessment", score_assessment)
    graph.add_node("generate_insights", generate_insights)
    graph.add_node("prioritize_actions", prioritize_actions)
    graph.add_node("build_30_60_90_plan", build_30_60_90_plan)
    graph.add_node("persist_results", persist_results)

    graph.add_edge(START, "validate_inputs")
    graph.add_edge("validate_inputs", "normalize_profile")
    graph.add_edge("normalize_profile", "retrieve_knowledge")
    graph.add_edge("retrieve_knowledge", "score_assessment")
    graph.add_edge("score_assessment", "generate_insights")
    graph.add_edge("generate_insights", "prioritize_actions")
    graph.add_edge("prioritize_actions", "build_30_60_90_plan")
    graph.add_edge("build_30_60_90_plan", "persist_results")
    graph.add_edge("persist_results", END)

    return graph.compile()

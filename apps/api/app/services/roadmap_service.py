from datetime import UTC, datetime
from uuid import uuid4

from app.repositories.roadmap_repository import roadmap_repository
from app.schemas.analysis import PriorityRecommendation
from app.schemas.roadmap import RoadmapAction, RoadmapRead
from app.services.analysis_service import analysis_service


def build_phase_action(
    priority: PriorityRecommendation,
    phase_title: str,
    phase_description: str,
) -> RoadmapAction:
    return RoadmapAction(
        title=phase_title,
        description=phase_description.format(priority_title=priority.title.lower()),
        why_it_matters=priority.why,
        effort=priority.effort,
        cost_band=priority.cost_band,
        expected_impact=priority.expected_impact,
    )


def build_risk_action(risk_text: str, title: str) -> RoadmapAction:
    return RoadmapAction(
        title=title,
        description=f"Review the underlying issue behind: {risk_text}",
        why_it_matters="Addressing the most visible risk early helps the business improve execution confidence.",
        effort="medium",
        cost_band="low",
        expected_impact="medium",
    )


def priority_for_index(priorities: list[PriorityRecommendation], index: int) -> PriorityRecommendation:
    if index < len(priorities):
        return priorities[index]
    return priorities[-1]


class RoadmapService:
    """Deterministic roadmap generation from the saved analysis summary."""

    def get_roadmap(self, user_id: str) -> RoadmapRead | None:
        return roadmap_repository.get(user_id)

    def generate_roadmap(self, user_id: str) -> RoadmapRead | None:
        analysis = analysis_service.get_analysis(user_id)
        if analysis is None:
            return None

        priorities = analysis.top_priorities
        risks = analysis.top_risks

        first_priority = priority_for_index(priorities, 0)
        second_priority = priority_for_index(priorities, min(1, len(priorities) - 1))
        third_priority = priority_for_index(priorities, min(2, len(priorities) - 1))

        days0to30 = [
            build_phase_action(
                first_priority,
                first_priority.title,
                "Start the first execution cycle for {priority_title} and define the minimum repeatable process.",
            )
        ]

        days31to60 = [
            build_phase_action(
                second_priority,
                f"Operationalize {second_priority.title.lower()}",
                "Move from setup into weekly execution for {priority_title}, with clearer tracking and ownership.",
            )
        ]

        days61to90 = [
            build_phase_action(
                third_priority,
                f"Scale {third_priority.title.lower()}",
                "Use the initial learning period to strengthen and extend {priority_title} across the business.",
            )
        ]

        if risks:
            days0to30.append(build_risk_action(risks[0], "Stabilize the most urgent risk"))
        if len(risks) > 1:
            days31to60.append(build_risk_action(risks[1], "Reduce execution friction"))
        if len(risks) > 2:
            days61to90.append(build_risk_action(risks[2], "Prevent recurring bottlenecks"))

        roadmap = RoadmapRead(
            id=f"roadmap_{uuid4().hex}",
            analysis_id=analysis.id,
            days0to30=days0to30,
            days31to60=days31to60,
            days61to90=days61to90,
            created_at=datetime.now(UTC).isoformat(),
        )

        return roadmap_repository.save(roadmap, user_id)


roadmap_service = RoadmapService()

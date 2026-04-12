from sqlalchemy import select, update

from app.db.session import session_scope
from app.models.roadmap import RoadmapRecord
from app.schemas.roadmap import RoadmapAction, RoadmapRead


def _to_schema(record: RoadmapRecord) -> RoadmapRead:
    return RoadmapRead(
        id=record.id,
        analysis_id=record.analysis_id,
        days0to30=[RoadmapAction.model_validate(item) for item in record.days_0_to_30 or []],
        days31to60=[RoadmapAction.model_validate(item) for item in record.days_31_to_60 or []],
        days61to90=[RoadmapAction.model_validate(item) for item in record.days_61_to_90 or []],
        created_at=record.created_at.isoformat(),
    )


class RoadmapRepository:
    """PostgreSQL-backed repository for generated roadmaps."""

    def get(self, user_id: str) -> RoadmapRead | None:
        with session_scope() as session:
            record = session.scalar(
                select(RoadmapRecord)
                .where(RoadmapRecord.user_id == user_id)
                .where(RoadmapRecord.is_active.is_(True))
                .order_by(RoadmapRecord.created_at.desc())
                .limit(1)
            )
            if record is None:
                return None
            return _to_schema(record)

    def save(self, roadmap: RoadmapRead, user_id: str) -> RoadmapRead:
        with session_scope() as session:
            session.execute(
                update(RoadmapRecord)
                .where(RoadmapRecord.user_id == user_id)
                .where(RoadmapRecord.is_active.is_(True))
                .values(is_active=False)
            )
            record = RoadmapRecord(
                id=roadmap.id,
                user_id=user_id,
                analysis_id=roadmap.analysis_id,
                days_0_to_30=[item.model_dump(mode="json") for item in roadmap.days0to30],
                days_31_to_60=[item.model_dump(mode="json") for item in roadmap.days31to60],
                days_61_to_90=[item.model_dump(mode="json") for item in roadmap.days61to90],
            )
            session.add(record)
            session.flush()
            session.refresh(record)
            return _to_schema(record)


roadmap_repository = RoadmapRepository()

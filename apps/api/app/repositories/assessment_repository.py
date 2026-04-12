from datetime import datetime

from sqlalchemy import select
from sqlalchemy.orm import selectinload

from app.db.session import session_scope
from app.models.assessment import AssessmentAnswerRecord, AssessmentRecord
from app.schemas.assessment import AssessmentAnswer, AssessmentRead, AssessmentSection

DEFAULT_BUSINESS_ID = "business_profile_v1"


def _to_answer_schema(record: AssessmentAnswerRecord) -> AssessmentAnswer:
    return AssessmentAnswer(
        question_key=record.question_key,
        section_key=record.section_key,
        answer_type=record.answer_type,
        value=record.value,
    )


def _to_datetime(value: str | None) -> datetime | None:
    if value is None:
        return None
    return datetime.fromisoformat(value)


def _to_schema(record: AssessmentRecord) -> AssessmentRead:
    return AssessmentRead(
        id=record.id,
        business_id=record.business_profile_id or DEFAULT_BUSINESS_ID,
        status=record.status,
        version=record.version,
        started_at=record.started_at.isoformat(),
        submitted_at=record.submitted_at.isoformat() if record.submitted_at else None,
        sections=[AssessmentSection.model_validate(section) for section in record.sections],
        answers=[_to_answer_schema(answer) for answer in sorted(record.answers, key=lambda item: item.order_index)],
    )


class AssessmentRepository:
    """PostgreSQL-backed repository for the single active assessment."""

    def get(self) -> AssessmentRead | None:
        with session_scope() as session:
            record = session.scalar(
                select(AssessmentRecord)
                .options(selectinload(AssessmentRecord.answers))
                .where(AssessmentRecord.is_active.is_(True))
                .order_by(AssessmentRecord.updated_at.desc())
                .limit(1)
            )
            if record is None:
                return None
            return _to_schema(record)

    def create(self, assessment: AssessmentRead) -> AssessmentRead:
        with session_scope() as session:
            record = AssessmentRecord(
                id=assessment.id,
                user_id=None,
                business_profile_id=None
                if assessment.business_id == DEFAULT_BUSINESS_ID
                else assessment.business_id,
                status=assessment.status,
                version=assessment.version,
                started_at=_to_datetime(assessment.started_at),
                submitted_at=_to_datetime(assessment.submitted_at),
                sections=[section.model_dump(mode="json") for section in assessment.sections],
            )
            session.add(record)
            session.flush()
            record.answers = [
                AssessmentAnswerRecord(
                    assessment_id=record.id,
                    user_id=None,
                    order_index=index,
                    question_key=answer.question_key,
                    section_key=answer.section_key,
                    answer_type=answer.answer_type,
                    value=answer.value,
                )
                for index, answer in enumerate(assessment.answers)
            ]
            session.flush()
            session.refresh(record)
            return _to_schema(record)

    def update(self, assessment: AssessmentRead) -> AssessmentRead:
        with session_scope() as session:
            record = session.scalar(
                select(AssessmentRecord)
                .options(selectinload(AssessmentRecord.answers))
                .where(AssessmentRecord.id == assessment.id)
                .limit(1)
            )
            if record is None:
                raise ValueError(f"Assessment {assessment.id} not found")

            record.status = assessment.status
            record.version = assessment.version
            record.started_at = _to_datetime(assessment.started_at)
            record.submitted_at = _to_datetime(assessment.submitted_at)
            record.sections = [section.model_dump(mode="json") for section in assessment.sections]
            record.business_profile_id = (
                None if assessment.business_id == DEFAULT_BUSINESS_ID else assessment.business_id
            )
            record.answers.clear()
            session.flush()
            record.answers = [
                AssessmentAnswerRecord(
                    assessment_id=record.id,
                    user_id=record.user_id,
                    order_index=index,
                    question_key=answer.question_key,
                    section_key=answer.section_key,
                    answer_type=answer.answer_type,
                    value=answer.value,
                )
                for index, answer in enumerate(assessment.answers)
            ]
            session.flush()
            session.refresh(record)
            return _to_schema(record)


assessment_repository = AssessmentRepository()

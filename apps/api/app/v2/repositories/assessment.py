from datetime import datetime

from sqlalchemy import select
from sqlalchemy.orm import selectinload

from app.db.session import session_scope
from app.models.assessment_v2 import AssessmentAnswerV2Record, AssessmentV2Record
from app.v2.schemas.assessment import AssessmentAnswerRead, AssessmentRead


def _to_datetime(value: str | None) -> datetime | None:
    if value is None:
        return None
    return datetime.fromisoformat(value)


def _to_answer_schema(record: AssessmentAnswerV2Record) -> AssessmentAnswerRead:
    return AssessmentAnswerRead(
        question_id=record.question_id,
        section_id=record.section_id,
        module_id=record.module_id,
        answer_type=record.answer_type,
        response_kind=record.response_kind,
        value=record.value,
        is_sufficient_answer=record.is_sufficient_answer,
        order_index=record.order_index,
    )


def _to_schema(record: AssessmentV2Record) -> AssessmentRead:
    return AssessmentRead(
        id=record.id,
        business_profile_v2_id=record.business_profile_v2_id,
        question_bank_version=record.question_bank_version,
        status=record.status,
        completeness_hint=record.completeness_hint,
        latest_definition_snapshot=record.latest_definition_snapshot,
        started_at=record.started_at.isoformat(),
        submitted_at=record.submitted_at.isoformat() if record.submitted_at else None,
        answers=[_to_answer_schema(answer) for answer in sorted(record.answers, key=lambda item: item.order_index or 0)],
    )


class AssessmentV2Repository:
    def get_latest(self, user_id: str) -> AssessmentRead | None:
        with session_scope() as session:
            record = session.scalar(
                select(AssessmentV2Record)
                .options(selectinload(AssessmentV2Record.answers))
                .where(AssessmentV2Record.user_id == user_id)
                .order_by(AssessmentV2Record.updated_at.desc())
                .limit(1)
            )
            if record is None:
                return None
            return _to_schema(record)

    def get_by_id(self, assessment_id: str, user_id: str) -> AssessmentRead | None:
        with session_scope() as session:
            record = session.scalar(
                select(AssessmentV2Record)
                .options(selectinload(AssessmentV2Record.answers))
                .where(AssessmentV2Record.id == assessment_id)
                .where(AssessmentV2Record.user_id == user_id)
                .limit(1)
            )
            if record is None:
                return None
            return _to_schema(record)

    def save(self, assessment: AssessmentRead, user_id: str) -> AssessmentRead:
        with session_scope() as session:
            record = session.scalar(
                select(AssessmentV2Record)
                .options(selectinload(AssessmentV2Record.answers))
                .where(AssessmentV2Record.id == assessment.id)
                .where(AssessmentV2Record.user_id == user_id)
                .limit(1)
            )

            if record is None:
                record = AssessmentV2Record(
                    id=assessment.id,
                    user_id=user_id,
                    business_profile_v2_id=assessment.business_profile_v2_id,
                    question_bank_version=assessment.question_bank_version,
                    status=assessment.status,
                    completeness_hint=assessment.completeness_hint,
                    latest_definition_snapshot=assessment.latest_definition_snapshot,
                    started_at=_to_datetime(assessment.started_at),
                    submitted_at=_to_datetime(assessment.submitted_at),
                )
                session.add(record)
                session.flush()
            else:
                record.business_profile_v2_id = assessment.business_profile_v2_id
                record.question_bank_version = assessment.question_bank_version
                record.status = assessment.status
                record.completeness_hint = assessment.completeness_hint
                record.latest_definition_snapshot = assessment.latest_definition_snapshot
                record.started_at = _to_datetime(assessment.started_at)
                record.submitted_at = _to_datetime(assessment.submitted_at)
                record.answers.clear()
                session.flush()

            record.answers = [
                AssessmentAnswerV2Record(
                    assessment_id=record.id,
                    question_id=answer.question_id,
                    section_id=answer.section_id,
                    module_id=answer.module_id,
                    answer_type=answer.answer_type,
                    response_kind=answer.response_kind,
                    value=answer.value,
                    is_sufficient_answer=answer.is_sufficient_answer,
                    order_index=answer.order_index,
                )
                for answer in assessment.answers
            ]
            session.flush()
            session.refresh(record)
            return _to_schema(record)


assessment_v2_repository = AssessmentV2Repository()

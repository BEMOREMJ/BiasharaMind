from datetime import datetime
from typing import Any

from sqlalchemy import DateTime, ForeignKey, Integer, String, func
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class AssessmentV2Record(Base):
    __tablename__ = "assessments_v2"

    id: Mapped[str] = mapped_column(String(64), primary_key=True)
    user_id: Mapped[str | None] = mapped_column(String(128), nullable=True, index=True)
    business_profile_v2_id: Mapped[str | None] = mapped_column(
        ForeignKey("business_profiles_v2.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )
    question_bank_version: Mapped[str] = mapped_column(String(64), nullable=False)
    status: Mapped[str] = mapped_column(String(32), nullable=False, index=True)
    completeness_hint: Mapped[str | None] = mapped_column(String(64), nullable=True)
    latest_definition_snapshot: Mapped[dict[str, Any] | None] = mapped_column(JSONB, nullable=True)
    started_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    submitted_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

    answers = relationship(
        "AssessmentAnswerV2Record",
        back_populates="assessment",
        cascade="all, delete-orphan",
        order_by="AssessmentAnswerV2Record.order_index",
    )


class AssessmentAnswerV2Record(Base):
    __tablename__ = "assessment_answers_v2"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    assessment_id: Mapped[str] = mapped_column(
        ForeignKey("assessments_v2.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    question_id: Mapped[str] = mapped_column(String(64), nullable=False, index=True)
    section_id: Mapped[str] = mapped_column(String(64), nullable=False, index=True)
    module_id: Mapped[str | None] = mapped_column(String(64), nullable=True)
    answer_type: Mapped[str] = mapped_column(String(32), nullable=False)
    response_kind: Mapped[str] = mapped_column(String(32), nullable=False)
    value: Mapped[str | int | float | list[str] | None] = mapped_column(JSONB, nullable=True)
    is_sufficient_answer: Mapped[bool | None] = mapped_column(nullable=True)
    order_index: Mapped[int | None] = mapped_column(Integer, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

    assessment = relationship("AssessmentV2Record", back_populates="answers")

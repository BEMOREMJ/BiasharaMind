from datetime import datetime
from typing import Any

from sqlalchemy import Boolean, DateTime, ForeignKey, Numeric, String, func
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class AnalysisRecord(Base):
    __tablename__ = "analyses"

    id: Mapped[str] = mapped_column(String(64), primary_key=True)
    user_id: Mapped[str | None] = mapped_column(String(128), nullable=True, index=True)
    assessment_id: Mapped[str] = mapped_column(
        ForeignKey("assessments.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    overall_score: Mapped[float] = mapped_column(Numeric(5, 2), nullable=False)
    category_scores: Mapped[list[dict[str, Any]]] = mapped_column(JSONB, default=list)
    top_strengths: Mapped[list[str]] = mapped_column(JSONB, default=list)
    top_risks: Mapped[list[str]] = mapped_column(JSONB, default=list)
    top_priorities: Mapped[list[dict[str, Any]]] = mapped_column(JSONB, default=list)
    model_version: Mapped[str] = mapped_column(String(64), nullable=False)
    workflow_version: Mapped[str] = mapped_column(String(64), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False, index=True)
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

    assessment = relationship("AssessmentRecord", back_populates="analyses")
    roadmaps = relationship("RoadmapRecord", back_populates="analysis")
    reports = relationship("ReportRecord", back_populates="analysis")

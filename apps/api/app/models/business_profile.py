from datetime import datetime

from sqlalchemy import Boolean, DateTime, String, Text, func
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class BusinessProfileRecord(Base):
    __tablename__ = "business_profiles"

    id: Mapped[str] = mapped_column(String(64), primary_key=True)
    user_id: Mapped[str | None] = mapped_column(String(128), nullable=True, index=True)
    business_name: Mapped[str] = mapped_column(String(120))
    industry: Mapped[str] = mapped_column(String(80))
    country: Mapped[str] = mapped_column(String(2))
    size_band: Mapped[str] = mapped_column(String(40))
    years_operating: Mapped[int] = mapped_column()
    revenue_band: Mapped[str] = mapped_column(String(40))
    team_size: Mapped[int] = mapped_column()
    main_goal: Mapped[str] = mapped_column(Text)
    budget_band: Mapped[str] = mapped_column(String(40))
    current_tools: Mapped[list[str]] = mapped_column(JSONB, default=list)
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

    assessments = relationship("AssessmentRecord", back_populates="business_profile")

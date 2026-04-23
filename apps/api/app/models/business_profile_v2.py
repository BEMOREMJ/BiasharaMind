from datetime import datetime

from sqlalchemy import DateTime, Integer, String, Text, func
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class BusinessProfileV2Record(Base):
    __tablename__ = "business_profiles_v2"

    id: Mapped[str] = mapped_column(String(64), primary_key=True)
    user_id: Mapped[str | None] = mapped_column(String(128), nullable=True, index=True)
    business_name: Mapped[str] = mapped_column(String(120), nullable=False)
    primary_business_type: Mapped[str] = mapped_column(String(64), nullable=False)
    main_offer: Mapped[str] = mapped_column(Text, nullable=False)
    customer_type: Mapped[str] = mapped_column(String(64), nullable=False)
    sales_channels: Mapped[list[str]] = mapped_column(JSONB, nullable=False, default=list)
    fulfilment_model: Mapped[str] = mapped_column(String(64), nullable=False)
    inventory_involvement: Mapped[str] = mapped_column(String(64), nullable=False)
    credit_sales_exposure: Mapped[str] = mapped_column(String(64), nullable=False)
    business_age_stage: Mapped[str] = mapped_column(String(64), nullable=False)
    team_size_band: Mapped[str] = mapped_column(String(64), nullable=False)
    number_of_locations: Mapped[int] = mapped_column(Integer, nullable=False)
    monthly_revenue_band: Mapped[str] = mapped_column(String(64), nullable=False)
    seasonality_level: Mapped[str | None] = mapped_column(String(64), nullable=True)
    peak_periods: Mapped[list[str] | None] = mapped_column(JSONB, nullable=True)
    owner_involvement_level: Mapped[str] = mapped_column(String(64), nullable=False)
    primary_business_goal: Mapped[str] = mapped_column(String(64), nullable=False)
    time_capacity: Mapped[str] = mapped_column(String(64), nullable=False)
    budget_flexibility: Mapped[str] = mapped_column(String(64), nullable=False)
    tool_hire_openness: Mapped[str] = mapped_column(String(64), nullable=False)
    record_availability: Mapped[str] = mapped_column(String(64), nullable=False)
    compliance_sector_sensitivity: Mapped[str | None] = mapped_column(String(64), nullable=True)
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

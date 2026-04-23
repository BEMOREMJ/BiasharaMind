"""add v2 business profiles table

Revision ID: 20260423_0003
Revises: 20260423_0002
Create Date: 2026-04-23 13:30:00
"""
from __future__ import annotations

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


revision = "20260423_0003"
down_revision = "20260423_0002"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "business_profiles_v2",
        sa.Column("id", sa.String(length=64), nullable=False),
        sa.Column("user_id", sa.String(length=128), nullable=True),
        sa.Column("business_name", sa.String(length=120), nullable=False),
        sa.Column("primary_business_type", sa.String(length=64), nullable=False),
        sa.Column("main_offer", sa.Text(), nullable=False),
        sa.Column("customer_type", sa.String(length=64), nullable=False),
        sa.Column(
            "sales_channels",
            postgresql.JSONB(astext_type=sa.Text()),
            nullable=False,
            server_default=sa.text("'[]'::jsonb"),
        ),
        sa.Column("fulfilment_model", sa.String(length=64), nullable=False),
        sa.Column("inventory_involvement", sa.String(length=64), nullable=False),
        sa.Column("credit_sales_exposure", sa.String(length=64), nullable=False),
        sa.Column("business_age_stage", sa.String(length=64), nullable=False),
        sa.Column("team_size_band", sa.String(length=64), nullable=False),
        sa.Column("number_of_locations", sa.Integer(), nullable=False),
        sa.Column("monthly_revenue_band", sa.String(length=64), nullable=False),
        sa.Column("seasonality_level", sa.String(length=64), nullable=True),
        sa.Column("peak_periods", postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column("owner_involvement_level", sa.String(length=64), nullable=False),
        sa.Column("primary_business_goal", sa.String(length=64), nullable=False),
        sa.Column("time_capacity", sa.String(length=64), nullable=False),
        sa.Column("budget_flexibility", sa.String(length=64), nullable=False),
        sa.Column("tool_hire_openness", sa.String(length=64), nullable=False),
        sa.Column("record_availability", sa.String(length=64), nullable=False),
        sa.Column("compliance_sector_sensitivity", sa.String(length=64), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_business_profiles_v2")),
    )
    op.create_index(op.f("ix_business_profiles_v2_user_id"), "business_profiles_v2", ["user_id"], unique=False)


def downgrade() -> None:
    op.drop_index(op.f("ix_business_profiles_v2_user_id"), table_name="business_profiles_v2")
    op.drop_table("business_profiles_v2")

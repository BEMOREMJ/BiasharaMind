"""add v2 refs to analysis runs

Revision ID: 20260423_0005
Revises: 20260423_0004
Create Date: 2026-04-23 20:00:00
"""
from __future__ import annotations

from alembic import op
import sqlalchemy as sa


revision = "20260423_0005"
down_revision = "20260423_0004"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column("analysis_runs", sa.Column("business_profile_v2_id", sa.String(length=64), nullable=True))
    op.add_column("analysis_runs", sa.Column("assessment_v2_id", sa.String(length=64), nullable=True))
    op.create_foreign_key(
        op.f("fk_analysis_runs_business_profile_v2_id_business_profiles_v2"),
        "analysis_runs",
        "business_profiles_v2",
        ["business_profile_v2_id"],
        ["id"],
        ondelete="SET NULL",
    )
    op.create_foreign_key(
        op.f("fk_analysis_runs_assessment_v2_id_assessments_v2"),
        "analysis_runs",
        "assessments_v2",
        ["assessment_v2_id"],
        ["id"],
        ondelete="SET NULL",
    )
    op.create_index(op.f("ix_analysis_runs_business_profile_v2_id"), "analysis_runs", ["business_profile_v2_id"], unique=False)
    op.create_index(op.f("ix_analysis_runs_assessment_v2_id"), "analysis_runs", ["assessment_v2_id"], unique=False)


def downgrade() -> None:
    op.drop_index(op.f("ix_analysis_runs_assessment_v2_id"), table_name="analysis_runs")
    op.drop_index(op.f("ix_analysis_runs_business_profile_v2_id"), table_name="analysis_runs")
    op.drop_constraint(op.f("fk_analysis_runs_assessment_v2_id_assessments_v2"), "analysis_runs", type_="foreignkey")
    op.drop_constraint(op.f("fk_analysis_runs_business_profile_v2_id_business_profiles_v2"), "analysis_runs", type_="foreignkey")
    op.drop_column("analysis_runs", "assessment_v2_id")
    op.drop_column("analysis_runs", "business_profile_v2_id")

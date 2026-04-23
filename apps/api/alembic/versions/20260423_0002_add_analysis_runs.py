"""add v2 analysis runs table

Revision ID: 20260423_0002
Revises: 20260412_0001
Create Date: 2026-04-23 10:30:00
"""
from __future__ import annotations

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


revision = "20260423_0002"
down_revision = "20260412_0001"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "analysis_runs",
        sa.Column("id", sa.String(length=64), nullable=False),
        sa.Column("user_id", sa.String(length=128), nullable=True),
        sa.Column("business_profile_id", sa.String(length=64), nullable=True),
        sa.Column("assessment_id", sa.String(length=64), nullable=True),
        sa.Column("analysis_family", sa.String(length=64), nullable=False),
        sa.Column("question_bank_version", sa.String(length=64), nullable=False),
        sa.Column("scoring_version", sa.String(length=64), nullable=False),
        sa.Column("taxonomy_version", sa.String(length=64), nullable=False),
        sa.Column("prompt_version", sa.String(length=64), nullable=True),
        sa.Column("analysis_engine_version", sa.String(length=64), nullable=False),
        sa.Column("freshness_status", sa.String(length=64), nullable=False),
        sa.Column("rerun_required", sa.Boolean(), nullable=False, server_default=sa.text("false")),
        sa.Column("rerun_reason", sa.String(length=64), nullable=True),
        sa.Column("ai_interpretation_status", sa.String(length=64), nullable=False),
        sa.Column("snapshot_payload", postgresql.JSONB(astext_type=sa.Text()), nullable=False, server_default=sa.text("'{}'::jsonb")),
        sa.Column("notes", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
        sa.ForeignKeyConstraint(
            ["assessment_id"],
            ["assessments.id"],
            name=op.f("fk_analysis_runs_assessment_id_assessments"),
            ondelete="SET NULL",
        ),
        sa.ForeignKeyConstraint(
            ["business_profile_id"],
            ["business_profiles.id"],
            name=op.f("fk_analysis_runs_business_profile_id_business_profiles"),
            ondelete="SET NULL",
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_analysis_runs")),
    )
    op.create_index(op.f("ix_analysis_runs_analysis_family"), "analysis_runs", ["analysis_family"], unique=False)
    op.create_index(op.f("ix_analysis_runs_assessment_id"), "analysis_runs", ["assessment_id"], unique=False)
    op.create_index(op.f("ix_analysis_runs_business_profile_id"), "analysis_runs", ["business_profile_id"], unique=False)
    op.create_index(op.f("ix_analysis_runs_freshness_status"), "analysis_runs", ["freshness_status"], unique=False)
    op.create_index(op.f("ix_analysis_runs_user_id"), "analysis_runs", ["user_id"], unique=False)


def downgrade() -> None:
    op.drop_index(op.f("ix_analysis_runs_user_id"), table_name="analysis_runs")
    op.drop_index(op.f("ix_analysis_runs_freshness_status"), table_name="analysis_runs")
    op.drop_index(op.f("ix_analysis_runs_business_profile_id"), table_name="analysis_runs")
    op.drop_index(op.f("ix_analysis_runs_assessment_id"), table_name="analysis_runs")
    op.drop_index(op.f("ix_analysis_runs_analysis_family"), table_name="analysis_runs")
    op.drop_table("analysis_runs")

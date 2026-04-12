"""initial postgres persistence

Revision ID: 20260412_0001
Revises:
Create Date: 2026-04-12 13:05:00
"""
from __future__ import annotations

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


revision = "20260412_0001"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "business_profiles",
        sa.Column("id", sa.String(length=64), nullable=False),
        sa.Column("user_id", sa.String(length=128), nullable=True),
        sa.Column("business_name", sa.String(length=120), nullable=False),
        sa.Column("industry", sa.String(length=80), nullable=False),
        sa.Column("country", sa.String(length=2), nullable=False),
        sa.Column("size_band", sa.String(length=40), nullable=False),
        sa.Column("years_operating", sa.Integer(), nullable=False),
        sa.Column("revenue_band", sa.String(length=40), nullable=False),
        sa.Column("team_size", sa.Integer(), nullable=False),
        sa.Column("main_goal", sa.Text(), nullable=False),
        sa.Column("budget_band", sa.String(length=40), nullable=False),
        sa.Column(
            "current_tools",
            postgresql.JSONB(astext_type=sa.Text()),
            nullable=False,
            server_default=sa.text("'[]'::jsonb"),
        ),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default=sa.text("true")),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_business_profiles")),
    )
    op.create_index(op.f("ix_business_profiles_is_active"), "business_profiles", ["is_active"], unique=False)
    op.create_index(op.f("ix_business_profiles_user_id"), "business_profiles", ["user_id"], unique=False)

    op.create_table(
        "assessments",
        sa.Column("id", sa.String(length=64), nullable=False),
        sa.Column("user_id", sa.String(length=128), nullable=True),
        sa.Column("business_profile_id", sa.String(length=64), nullable=True),
        sa.Column("status", sa.String(length=32), nullable=False),
        sa.Column("version", sa.String(length=32), nullable=False),
        sa.Column("started_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("submitted_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column(
            "sections",
            postgresql.JSONB(astext_type=sa.Text()),
            nullable=False,
            server_default=sa.text("'[]'::jsonb"),
        ),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default=sa.text("true")),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
        sa.ForeignKeyConstraint(
            ["business_profile_id"],
            ["business_profiles.id"],
            name=op.f("fk_assessments_business_profile_id_business_profiles"),
            ondelete="SET NULL",
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_assessments")),
    )
    op.create_index(op.f("ix_assessments_business_profile_id"), "assessments", ["business_profile_id"], unique=False)
    op.create_index(op.f("ix_assessments_is_active"), "assessments", ["is_active"], unique=False)
    op.create_index(op.f("ix_assessments_status"), "assessments", ["status"], unique=False)
    op.create_index(op.f("ix_assessments_user_id"), "assessments", ["user_id"], unique=False)

    op.create_table(
        "assessment_answers",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("assessment_id", sa.String(length=64), nullable=False),
        sa.Column("user_id", sa.String(length=128), nullable=True),
        sa.Column("order_index", sa.Integer(), nullable=False),
        sa.Column("question_key", sa.String(length=64), nullable=False),
        sa.Column("section_key", sa.String(length=64), nullable=False),
        sa.Column("answer_type", sa.String(length=20), nullable=False),
        sa.Column("value", postgresql.JSONB(astext_type=sa.Text()), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
        sa.ForeignKeyConstraint(
            ["assessment_id"],
            ["assessments.id"],
            name=op.f("fk_assessment_answers_assessment_id_assessments"),
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_assessment_answers")),
    )
    op.create_index(op.f("ix_assessment_answers_assessment_id"), "assessment_answers", ["assessment_id"], unique=False)
    op.create_index(op.f("ix_assessment_answers_section_key"), "assessment_answers", ["section_key"], unique=False)
    op.create_index(op.f("ix_assessment_answers_user_id"), "assessment_answers", ["user_id"], unique=False)

    op.create_table(
        "analyses",
        sa.Column("id", sa.String(length=64), nullable=False),
        sa.Column("user_id", sa.String(length=128), nullable=True),
        sa.Column("assessment_id", sa.String(length=64), nullable=False),
        sa.Column("overall_score", sa.Numeric(precision=5, scale=2), nullable=False),
        sa.Column(
            "category_scores",
            postgresql.JSONB(astext_type=sa.Text()),
            nullable=False,
            server_default=sa.text("'[]'::jsonb"),
        ),
        sa.Column(
            "top_strengths",
            postgresql.JSONB(astext_type=sa.Text()),
            nullable=False,
            server_default=sa.text("'[]'::jsonb"),
        ),
        sa.Column(
            "top_risks",
            postgresql.JSONB(astext_type=sa.Text()),
            nullable=False,
            server_default=sa.text("'[]'::jsonb"),
        ),
        sa.Column(
            "top_priorities",
            postgresql.JSONB(astext_type=sa.Text()),
            nullable=False,
            server_default=sa.text("'[]'::jsonb"),
        ),
        sa.Column("model_version", sa.String(length=64), nullable=False),
        sa.Column("workflow_version", sa.String(length=64), nullable=False),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default=sa.text("true")),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
        sa.ForeignKeyConstraint(
            ["assessment_id"],
            ["assessments.id"],
            name=op.f("fk_analyses_assessment_id_assessments"),
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_analyses")),
    )
    op.create_index(op.f("ix_analyses_assessment_id"), "analyses", ["assessment_id"], unique=False)
    op.create_index(op.f("ix_analyses_is_active"), "analyses", ["is_active"], unique=False)
    op.create_index(op.f("ix_analyses_user_id"), "analyses", ["user_id"], unique=False)

    op.create_table(
        "roadmaps",
        sa.Column("id", sa.String(length=64), nullable=False),
        sa.Column("user_id", sa.String(length=128), nullable=True),
        sa.Column("analysis_id", sa.String(length=64), nullable=False),
        sa.Column(
            "days_0_to_30",
            postgresql.JSONB(astext_type=sa.Text()),
            nullable=False,
            server_default=sa.text("'[]'::jsonb"),
        ),
        sa.Column(
            "days_31_to_60",
            postgresql.JSONB(astext_type=sa.Text()),
            nullable=False,
            server_default=sa.text("'[]'::jsonb"),
        ),
        sa.Column(
            "days_61_to_90",
            postgresql.JSONB(astext_type=sa.Text()),
            nullable=False,
            server_default=sa.text("'[]'::jsonb"),
        ),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default=sa.text("true")),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
        sa.ForeignKeyConstraint(
            ["analysis_id"],
            ["analyses.id"],
            name=op.f("fk_roadmaps_analysis_id_analyses"),
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_roadmaps")),
    )
    op.create_index(op.f("ix_roadmaps_analysis_id"), "roadmaps", ["analysis_id"], unique=False)
    op.create_index(op.f("ix_roadmaps_is_active"), "roadmaps", ["is_active"], unique=False)
    op.create_index(op.f("ix_roadmaps_user_id"), "roadmaps", ["user_id"], unique=False)

    op.create_table(
        "reports",
        sa.Column("id", sa.String(length=64), nullable=False),
        sa.Column("user_id", sa.String(length=128), nullable=True),
        sa.Column("analysis_id", sa.String(length=64), nullable=False),
        sa.Column("format", sa.String(length=20), nullable=False),
        sa.Column("storage_path", sa.String(length=240), nullable=False),
        sa.Column("business_summary", postgresql.JSONB(astext_type=sa.Text()), nullable=False),
        sa.Column("overall_score", sa.Numeric(precision=5, scale=2), nullable=False),
        sa.Column(
            "category_scores",
            postgresql.JSONB(astext_type=sa.Text()),
            nullable=False,
            server_default=sa.text("'[]'::jsonb"),
        ),
        sa.Column(
            "strengths",
            postgresql.JSONB(astext_type=sa.Text()),
            nullable=False,
            server_default=sa.text("'[]'::jsonb"),
        ),
        sa.Column(
            "risks",
            postgresql.JSONB(astext_type=sa.Text()),
            nullable=False,
            server_default=sa.text("'[]'::jsonb"),
        ),
        sa.Column(
            "priorities",
            postgresql.JSONB(astext_type=sa.Text()),
            nullable=False,
            server_default=sa.text("'[]'::jsonb"),
        ),
        sa.Column(
            "roadmap_phases",
            postgresql.JSONB(astext_type=sa.Text()),
            nullable=False,
            server_default=sa.text("'[]'::jsonb"),
        ),
        sa.Column("export_file_name", sa.String(length=120), nullable=False),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default=sa.text("true")),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
        sa.ForeignKeyConstraint(
            ["analysis_id"],
            ["analyses.id"],
            name=op.f("fk_reports_analysis_id_analyses"),
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_reports")),
    )
    op.create_index(op.f("ix_reports_analysis_id"), "reports", ["analysis_id"], unique=False)
    op.create_index(op.f("ix_reports_is_active"), "reports", ["is_active"], unique=False)
    op.create_index(op.f("ix_reports_user_id"), "reports", ["user_id"], unique=False)


def downgrade() -> None:
    op.drop_index(op.f("ix_reports_user_id"), table_name="reports")
    op.drop_index(op.f("ix_reports_is_active"), table_name="reports")
    op.drop_index(op.f("ix_reports_analysis_id"), table_name="reports")
    op.drop_table("reports")

    op.drop_index(op.f("ix_roadmaps_user_id"), table_name="roadmaps")
    op.drop_index(op.f("ix_roadmaps_is_active"), table_name="roadmaps")
    op.drop_index(op.f("ix_roadmaps_analysis_id"), table_name="roadmaps")
    op.drop_table("roadmaps")

    op.drop_index(op.f("ix_analyses_user_id"), table_name="analyses")
    op.drop_index(op.f("ix_analyses_is_active"), table_name="analyses")
    op.drop_index(op.f("ix_analyses_assessment_id"), table_name="analyses")
    op.drop_table("analyses")

    op.drop_index(op.f("ix_assessment_answers_user_id"), table_name="assessment_answers")
    op.drop_index(op.f("ix_assessment_answers_section_key"), table_name="assessment_answers")
    op.drop_index(op.f("ix_assessment_answers_assessment_id"), table_name="assessment_answers")
    op.drop_table("assessment_answers")

    op.drop_index(op.f("ix_assessments_user_id"), table_name="assessments")
    op.drop_index(op.f("ix_assessments_status"), table_name="assessments")
    op.drop_index(op.f("ix_assessments_is_active"), table_name="assessments")
    op.drop_index(op.f("ix_assessments_business_profile_id"), table_name="assessments")
    op.drop_table("assessments")

    op.drop_index(op.f("ix_business_profiles_user_id"), table_name="business_profiles")
    op.drop_index(op.f("ix_business_profiles_is_active"), table_name="business_profiles")
    op.drop_table("business_profiles")

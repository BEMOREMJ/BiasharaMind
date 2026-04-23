"""add v2 assessments tables

Revision ID: 20260423_0004
Revises: 20260423_0003
Create Date: 2026-04-23 17:00:00
"""
from __future__ import annotations

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


revision = "20260423_0004"
down_revision = "20260423_0003"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "assessments_v2",
        sa.Column("id", sa.String(length=64), nullable=False),
        sa.Column("user_id", sa.String(length=128), nullable=True),
        sa.Column("business_profile_v2_id", sa.String(length=64), nullable=True),
        sa.Column("question_bank_version", sa.String(length=64), nullable=False),
        sa.Column("status", sa.String(length=32), nullable=False),
        sa.Column("completeness_hint", sa.String(length=64), nullable=True),
        sa.Column("latest_definition_snapshot", postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column("started_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("submitted_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
        sa.ForeignKeyConstraint(
            ["business_profile_v2_id"],
            ["business_profiles_v2.id"],
            name=op.f("fk_assessments_v2_business_profile_v2_id_business_profiles_v2"),
            ondelete="SET NULL",
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_assessments_v2")),
    )
    op.create_index(op.f("ix_assessments_v2_business_profile_v2_id"), "assessments_v2", ["business_profile_v2_id"], unique=False)
    op.create_index(op.f("ix_assessments_v2_status"), "assessments_v2", ["status"], unique=False)
    op.create_index(op.f("ix_assessments_v2_user_id"), "assessments_v2", ["user_id"], unique=False)

    op.create_table(
        "assessment_answers_v2",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("assessment_id", sa.String(length=64), nullable=False),
        sa.Column("question_id", sa.String(length=64), nullable=False),
        sa.Column("section_id", sa.String(length=64), nullable=False),
        sa.Column("module_id", sa.String(length=64), nullable=True),
        sa.Column("answer_type", sa.String(length=32), nullable=False),
        sa.Column("response_kind", sa.String(length=32), nullable=False),
        sa.Column("value", postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column("is_sufficient_answer", sa.Boolean(), nullable=True),
        sa.Column("order_index", sa.Integer(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
        sa.ForeignKeyConstraint(
            ["assessment_id"],
            ["assessments_v2.id"],
            name=op.f("fk_assessment_answers_v2_assessment_id_assessments_v2"),
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_assessment_answers_v2")),
    )
    op.create_index(op.f("ix_assessment_answers_v2_assessment_id"), "assessment_answers_v2", ["assessment_id"], unique=False)
    op.create_index(op.f("ix_assessment_answers_v2_question_id"), "assessment_answers_v2", ["question_id"], unique=False)
    op.create_index(op.f("ix_assessment_answers_v2_section_id"), "assessment_answers_v2", ["section_id"], unique=False)


def downgrade() -> None:
    op.drop_index(op.f("ix_assessment_answers_v2_section_id"), table_name="assessment_answers_v2")
    op.drop_index(op.f("ix_assessment_answers_v2_question_id"), table_name="assessment_answers_v2")
    op.drop_index(op.f("ix_assessment_answers_v2_assessment_id"), table_name="assessment_answers_v2")
    op.drop_table("assessment_answers_v2")

    op.drop_index(op.f("ix_assessments_v2_user_id"), table_name="assessments_v2")
    op.drop_index(op.f("ix_assessments_v2_status"), table_name="assessments_v2")
    op.drop_index(op.f("ix_assessments_v2_business_profile_v2_id"), table_name="assessments_v2")
    op.drop_table("assessments_v2")

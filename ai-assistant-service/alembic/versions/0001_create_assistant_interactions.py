"""create assistant_interactions table

Revision ID: 0001
Revises:
Create Date: 2026-05-12

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "0001"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "assistant_interactions",
        sa.Column("id", sa.String(length=36), primary_key=True),
        sa.Column("session_id", sa.String(length=128), nullable=False),
        sa.Column("user_question", sa.Text, nullable=False),
        sa.Column("interpreted_intent", sa.String(length=32), nullable=False),
        sa.Column("answer_text", sa.Text, nullable=False),
        sa.Column("created_at", sa.DateTime, nullable=False),
    )
    op.create_index(
        "ix_assistant_interactions_session_id",
        "assistant_interactions",
        ["session_id"],
    )
    op.create_index(
        "ix_assistant_interactions_session_created",
        "assistant_interactions",
        ["session_id", "created_at"],
    )


def downgrade() -> None:
    op.drop_index(
        "ix_assistant_interactions_session_created",
        table_name="assistant_interactions",
    )
    op.drop_index(
        "ix_assistant_interactions_session_id",
        table_name="assistant_interactions",
    )
    op.drop_table("assistant_interactions")
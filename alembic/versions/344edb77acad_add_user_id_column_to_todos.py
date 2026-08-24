"""add user_id column to todos

Revision ID: 344edb77acad
Revises: 636fe64617f4
Create Date: 2026-08-24 11:40:50.154988

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "344edb77acad"
down_revision: Union[str, Sequence[str], None] = "636fe64617f4"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""

    op.add_column(
        "todos",
        sa.Column(
            "user_id",
            sa.Integer(),
            nullable=True
        )
    )


def downgrade() -> None:
    """Downgrade schema."""

    op.drop_column(
        "todos",
        "user_id"
    )
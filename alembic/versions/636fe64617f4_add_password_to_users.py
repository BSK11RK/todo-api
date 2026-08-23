"""add password to users

Revision ID: 636fe64617f4
Revises: 17ff1f7ff701
Create Date: 2026-08-23 22:18:40.450862

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "636fe64617f4"
down_revision: Union[str, Sequence[str], None] = "17ff1f7ff701"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""

    op.add_column(
        "users",
        sa.Column(
            "password",
            sa.String(length=255),
            nullable=False
        )
    )


def downgrade() -> None:
    """Downgrade schema."""

    op.drop_column(
        "users",
        "password"
    )
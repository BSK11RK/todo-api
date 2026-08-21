"""add description and timestamps to todos

Revision ID: bc63e0a44ade
Revises: 5e7a132a4b18
Create Date: 2026-08-21 10:37:52.314201

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = 'bc63e0a44ade'
down_revision: Union[str, Sequence[str], None] = '5e7a132a4b18'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('todos', sa.Column('description', sa.Text(), nullable=False))
    op.add_column(
        'todos',
        sa.Column(
            'created_at',
            sa.DateTime(),
            server_default=sa.func.now(),   # ← DB側のデフォルト
            nullable=False
        )
    )
    op.add_column(
        'todos',
        sa.Column(
            'updated_at',
            sa.DateTime(),
            server_default=sa.func.now(),   # ← DB側のデフォルト
            nullable=False
        )
    )


def downgrade() -> None:
    op.drop_column('todos', 'updated_at')
    op.drop_column('todos', 'created_at')
    op.drop_column('todos', 'description')
"""add user_id to todos

Revision ID: 17ff1f7ff701
Revises: 0ba1d590ff51
Create Date: 2026-08-23 16:15:07.144051

"""

from typing import Sequence, Union

from alembic import op


# revision identifiers, used by Alembic.
revision: str = "17ff1f7ff701"

down_revision: Union[str, Sequence[str], None] = "0ba1d590ff51"

branch_labels: Union[str, Sequence[str], None] = None

depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""

    pass


def downgrade() -> None:
    """Downgrade schema."""

    pass
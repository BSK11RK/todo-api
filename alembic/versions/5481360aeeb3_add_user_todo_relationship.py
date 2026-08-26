"""add user todo relationship

Revision ID: 2cf22cceefde
Revises: 344edb77acad
Create Date: 2026-08-26 11:02:40.429736

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "2cf22cceefde"
down_revision: Union[str, Sequence[str], None] = "344edb77acad"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""

    with op.batch_alter_table("todos") as batch_op:
        batch_op.create_foreign_key(
            "fk_todos_user_id_users",
            "users",
            ["user_id"],
            ["id"],
            ondelete="CASCADE"
        )


def downgrade() -> None:
    """Downgrade schema."""

    with op.batch_alter_table("todos") as batch_op:
        batch_op.drop_constraint(
            "fk_todos_user_id_users",
            type_="foreignkey"
        )
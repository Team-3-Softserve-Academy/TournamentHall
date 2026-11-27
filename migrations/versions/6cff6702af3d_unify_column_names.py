"""unify column names

Revision ID: 6cff6702af3d
Revises: a307fdc4a238
Create Date: 2026-11-26 19:59:48.388579

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '6cff6702af3d'
down_revision: Union[str, Sequence[str], None] = 'a307fdc4a238'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.alter_column('knights', 'speed', new_column_name='dexterity')
    op.alter_column("knights", "home", new_column_name="house")
    op.alter_column("lords", "home", new_column_name="house")
    op.alter_column("commonfolks", "name", new_column_name="full_name")

    op.execute("UPDATE knights SET photo_url = NULL WHERE photo_url = 'default_photo_url'")
    op.execute("UPDATE lords SET photo_url = NULL WHERE photo_url = 'default_photo_url'")


def downgrade() -> None:
    op.alter_column("commonfolks", "full_name", new_column_name="name")
    op.alter_column("lords", "house", new_column_name="home")
    op.alter_column("knights", "house", new_column_name="home")
    op.alter_column("knights", "dexterity", new_column_name="speed")

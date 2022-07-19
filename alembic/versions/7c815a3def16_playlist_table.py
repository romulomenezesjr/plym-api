"""playlist table

Revision ID: 7c815a3def16
Revises: 5ffc580dce4a
Create Date: 2022-07-18 18:30:42.495156

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7c815a3def16'
down_revision = '5ffc580dce4a'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table("playlists", sa.Column("id", sa.Integer(), nullable=False, primary_key=True))


def downgrade() -> None:
    op.drop_table("playlists")

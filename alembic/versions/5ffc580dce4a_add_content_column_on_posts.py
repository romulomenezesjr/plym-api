"""add content column on posts

Revision ID: 5ffc580dce4a
Revises: f28068864779
Create Date: 2022-07-18 18:25:36.515365

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5ffc580dce4a'
down_revision = 'f28068864779'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column("posts", sa.Column("content", sa.String(255), nullable=False))


def downgrade() -> None:
    op.drop_column("posts", "content")

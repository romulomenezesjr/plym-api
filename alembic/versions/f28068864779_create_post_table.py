"""create post table

Revision ID: f28068864779
Revises: 
Create Date: 2022-07-18 18:20:35.047151

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f28068864779'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table("posts", sa.Column("id", sa.Integer(), nullable=False, primary_key=True))


def downgrade() -> None:
    op.drop_table("posts")

"""add columns to posts

Revision ID: 3cd5ab4cee30
Revises: cd8eb73d1319
Create Date: 2022-11-14 23:35:43.044708

"""
from alembic import op
import sqlalchemy as sa

from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.sql.expression import text

# revision identifiers, used by Alembic.
revision = '3cd5ab4cee30'
down_revision = 'cd8eb73d1319'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts', sa.Column('content', sa.String, nullable=False))
    op.add_column('posts', sa.Column('published', sa.Boolean, server_default='TRUE', nullable=False))
    op.add_column(
        'posts',
        sa.Column('created_at', TIMESTAMP(timezone=True), server_default=text('NOW()'), nullable=False)
    )


def downgrade():
    op.drop_column('posts', 'content')
    op.drop_column('posts', 'published')
    op.drop_column('posts', 'created_at')

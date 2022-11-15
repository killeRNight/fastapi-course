"""create posts table

Revision ID: cd8eb73d1319
Revises: 
Create Date: 2022-11-14 23:21:38.715551

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'cd8eb73d1319'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'posts',
        sa.Column('id', sa.Integer, nullable=False, primary_key=True),
        sa.Column('title', sa.String, nullable=False)
    )


def downgrade():
    op.drop_table('posts')

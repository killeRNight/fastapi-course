"""add foreign key to posts table

Revision ID: dc563767ac99
Revises: a7987d9d4e87
Create Date: 2022-11-15 00:41:45.663809

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'dc563767ac99'
down_revision = 'a7987d9d4e87'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts', sa.Column('owner_id', sa.Integer, nullable=False))
    op.create_foreign_key(
        'post_users_fk', source_table='posts',
        referent_table='users',
        local_cols=['owner_id'],
        remote_cols=['id'],
        ondelete="CASCADE"
    )


def downgrade():
    op.drop_constraint('post_users_fk', table_name='posts')
    op.drop_column('posts', 'owner_id')

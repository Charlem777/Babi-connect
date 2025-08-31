"""Add parent_id column to commentaire_offre for nested comments

Revision ID: add_parent_id_to_comments
Revises: add_comments_favorites
Create Date: 2025-08-30 14:45:00.000000

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = 'add_parent_id_to_comments'
down_revision = 'add_comments_favorites'
branch_labels = None
depends_on = None


def upgrade():
    # Add parent_id column to commentaire_offre table
    with op.batch_alter_table('commentaire_offre', schema=None) as batch_op:
        batch_op.add_column(sa.Column('parent_id', sa.Integer(), nullable=True))
        batch_op.create_foreign_key('fk_commentaire_parent', 'commentaire_offre', ['parent_id'], ['id'])


def downgrade():
    # Remove parent_id column from commentaire_offre table
    with op.batch_alter_table('commentaire_offre', schema=None) as batch_op:
        batch_op.drop_constraint('fk_commentaire_parent', type_='foreignkey')
        batch_op.drop_column('parent_id')

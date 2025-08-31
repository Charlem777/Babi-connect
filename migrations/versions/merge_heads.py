"""Merge multiple head revisions

Revision ID: merge_heads_001
Revises: chat_tables_001, fef542463f41
Create Date: 2025-08-30 12:46:00.000000

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = 'merge_heads_001'
down_revision = ('chat_tables_001', 'fef542463f41')
branch_labels = None
depends_on = None


def upgrade():
    # This is a merge migration - no changes needed
    pass


def downgrade():
    # This is a merge migration - no changes needed
    pass

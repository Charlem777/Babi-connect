"""Add favorites system and update comments date field

Revision ID: add_comments_favorites
Revises: merge_heads_001
Create Date: 2025-08-30 12:42:35.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'add_comments_favorites'
down_revision = 'merge_heads_001'
branch_labels = None
depends_on = None


def upgrade():
    # Create favori_offre table
    op.create_table('favori_offre',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('utilisateur_id', sa.Integer(), nullable=False),
        sa.Column('offre_id', sa.Integer(), nullable=False),
        sa.Column('date_ajout', sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(['offre_id'], ['offre.id'], ),
        sa.ForeignKeyConstraint(['utilisateur_id'], ['utilisateur.id'], ),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('utilisateur_id', 'offre_id', name='uq_favori_utilisateur_offre')
    )
    
    # Update commentaire_offre table - rename date to date_creation
    with op.batch_alter_table('commentaire_offre', schema=None) as batch_op:
        batch_op.add_column(sa.Column('date_creation', sa.DateTime(), nullable=True))
        
    # Copy data from date to date_creation
    op.execute("UPDATE commentaire_offre SET date_creation = date")
    
    # Drop old date column
    with op.batch_alter_table('commentaire_offre', schema=None) as batch_op:
        batch_op.drop_column('date')


def downgrade():
    # Add back date column to commentaire_offre
    with op.batch_alter_table('commentaire_offre', schema=None) as batch_op:
        batch_op.add_column(sa.Column('date', mysql.DATETIME(), nullable=True))
        
    # Copy data back
    op.execute("UPDATE commentaire_offre SET date = date_creation")
    
    # Drop date_creation column
    with op.batch_alter_table('commentaire_offre', schema=None) as batch_op:
        batch_op.drop_column('date_creation')
    
    # Drop favori_offre table
    op.drop_table('favori_offre')

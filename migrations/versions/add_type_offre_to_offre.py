"""Add type_offre to offre table

Revision ID: add_type_offre_to_offre
Revises: 
Create Date: 2025-08-31 16:50:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'add_type_offre_to_offre'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # Ajouter les champs promo et type_offre au modèle Offre
    with op.batch_alter_table('offre', schema=None) as batch_op:
        batch_op.add_column(sa.Column('type_offre', sa.String(length=50), nullable=False, default='service'))
        batch_op.add_column(sa.Column('is_promo', sa.Boolean(), nullable=True, default=False))
        batch_op.add_column(sa.Column('prix_original', sa.Float(), nullable=True))
        batch_op.add_column(sa.Column('pourcentage_reduction', sa.Integer(), nullable=True))
    
    # Mettre à jour les valeurs par défaut
    op.execute("UPDATE offre SET type_offre = 'service' WHERE type_offre IS NULL OR type_offre = ''")
    op.execute("UPDATE offre SET is_promo = FALSE WHERE is_promo IS NULL")


def downgrade():
    # Supprimer les colonnes ajoutées à offre
    with op.batch_alter_table('offre', schema=None) as batch_op:
        batch_op.drop_column('pourcentage_reduction')
        batch_op.drop_column('prix_original')
        batch_op.drop_column('is_promo')
        batch_op.drop_column('type_offre')

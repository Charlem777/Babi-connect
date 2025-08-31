"""Add promo fields to offre and type_offre to categorie_offre

Revision ID: add_promo_fields
Revises: 
Create Date: 2025-08-31 16:40:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'add_promo_fields'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # Ajouter les champs promo au modèle Offre
    with op.batch_alter_table('offre', schema=None) as batch_op:
        batch_op.add_column(sa.Column('is_promo', sa.Boolean(), nullable=True, default=False))
        batch_op.add_column(sa.Column('prix_original', sa.Float(), nullable=True))
        batch_op.add_column(sa.Column('pourcentage_reduction', sa.Integer(), nullable=True))
    
    # Ajouter les champs type_offre, icone et couleur au modèle CategorieOffre
    with op.batch_alter_table('categorie_offre', schema=None) as batch_op:
        batch_op.add_column(sa.Column('type_offre', sa.String(length=50), nullable=False, default='service'))
        batch_op.add_column(sa.Column('icone', sa.String(length=100), nullable=True))
        batch_op.add_column(sa.Column('couleur', sa.String(length=20), nullable=True))
    
    # Mettre à jour les valeurs par défaut
    op.execute("UPDATE offre SET is_promo = FALSE WHERE is_promo IS NULL")
    op.execute("UPDATE categorie_offre SET type_offre = 'service' WHERE type_offre IS NULL OR type_offre = ''")


def downgrade():
    # Supprimer les colonnes ajoutées à categorie_offre
    with op.batch_alter_table('categorie_offre', schema=None) as batch_op:
        batch_op.drop_column('couleur')
        batch_op.drop_column('icone')
        batch_op.drop_column('type_offre')
    
    # Supprimer les colonnes ajoutées à offre
    with op.batch_alter_table('offre', schema=None) as batch_op:
        batch_op.drop_column('pourcentage_reduction')
        batch_op.drop_column('prix_original')
        batch_op.drop_column('is_promo')

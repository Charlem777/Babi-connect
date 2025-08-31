"""Create chat tables

Revision ID: chat_tables_001
Revises: f7bf3d579513
Create Date: 2025-08-29 23:15:00.000000

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = 'chat_tables_001'
down_revision = 'f7bf3d579513'
depends_on = None

def upgrade():
    # Create conversation table
    op.create_table('conversation',
        sa.Column('id', sa.String(36), primary_key=True),
        sa.Column('client_id', sa.Integer, sa.ForeignKey('utilisateur.id'), nullable=True),
        sa.Column('partenaire_id', sa.Integer, sa.ForeignKey('partenaire.id'), nullable=False),
        sa.Column('guest_name', sa.String(100), nullable=True),
        sa.Column('guest_email', sa.String(120), nullable=True),
        sa.Column('sujet', sa.String(200), nullable=True),
        sa.Column('statut', sa.String(20), default='active'),
        sa.Column('date_creation', sa.DateTime, default=sa.func.now()),
        sa.Column('derniere_activite', sa.DateTime, default=sa.func.now())
    )

    # Create message table
    op.create_table('message',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('conversation_id', sa.String(36), sa.ForeignKey('conversation.id'), nullable=False),
        sa.Column('expediteur_type', sa.String(20), nullable=False),
        sa.Column('expediteur_id', sa.Integer, nullable=True),
        sa.Column('contenu', sa.Text, nullable=False),
        sa.Column('type_message', sa.String(20), default='text'),
        sa.Column('fichier_url', sa.String(500), nullable=True),
        sa.Column('lu', sa.Boolean, default=False),
        sa.Column('date_envoi', sa.DateTime, default=sa.func.now())
    )

    # Create indexes for better performance
    op.create_index('idx_conversation_partenaire', 'conversation', ['partenaire_id'])
    op.create_index('idx_conversation_client', 'conversation', ['client_id'])
    op.create_index('idx_conversation_activite', 'conversation', ['derniere_activite'])
    op.create_index('idx_message_conversation', 'message', ['conversation_id'])
    op.create_index('idx_message_date', 'message', ['date_envoi'])

def downgrade():
    # Drop indexes
    op.drop_index('idx_message_date')
    op.drop_index('idx_message_conversation')
    op.drop_index('idx_conversation_activite')
    op.drop_index('idx_conversation_client')
    op.drop_index('idx_conversation_partenaire')
    
    # Drop tables
    op.drop_table('message')
    op.drop_table('conversation')

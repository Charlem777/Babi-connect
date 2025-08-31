#!/usr/bin/env python3
"""
Script pour créer un utilisateur de test avec mot de passe hashé
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from backend.app import create_app
from backend.extensions import db
from backend.models import Utilisateur, Partenaire
from werkzeug.security import generate_password_hash

def seed_test_users():
    app = create_app()
    
    with app.app_context():
        print("🌱 Création des utilisateurs de test...")
        
        # Créer un utilisateur client de test
        test_user = Utilisateur.query.filter_by(email='test@babi.com').first()
        if not test_user:
            test_user = Utilisateur(
                nom='Test',
                prenom='User',
                email='test@babi.com',
                type_utilisateur='Client',
                mot_de_passe=generate_password_hash('password123', method='pbkdf2:sha256'),
                ville='Abidjan',
                commune='Cocody',
                telephone='0123456789'
            )
            db.session.add(test_user)
            print("✅ Utilisateur client créé: test@babi.com / password123")
        else:
            print("ℹ️ Utilisateur client existe déjà: test@babi.com")
        
        # Créer un partenaire de test
        test_partner = Partenaire.query.filter_by(email='partenaire@babi.com').first()
        if not test_partner:
            test_partner = Partenaire(
                nom='Restaurant Test',
                email='partenaire@babi.com',
                mot_de_passe=generate_password_hash('partner123', method='pbkdf2:sha256'),
                secteur_id=1,  # Assurez-vous qu'un secteur avec ID 1 existe
                categorie_partenaire_id=1,  # Assurez-vous qu'une catégorie avec ID 1 existe
                ville='Abidjan',
                commune='Plateau',
                description='Restaurant de test pour les démonstrations',
                contact='0987654321'
            )
            db.session.add(test_partner)
            print("✅ Partenaire créé: partenaire@babi.com / partner123")
        else:
            print("ℹ️ Partenaire existe déjà: partenaire@babi.com")
        
        # Créer un admin de test
        admin_user = Utilisateur.query.filter_by(email='admin@babi.com').first()
        if not admin_user:
            admin_user = Utilisateur(
                nom='Admin',
                prenom='System',
                email='admin@babi.com',
                type_utilisateur='Admin',
                mot_de_passe=generate_password_hash('admin123', method='pbkdf2:sha256'),
                ville='Abidjan',
                commune='Cocody'
            )
            db.session.add(admin_user)
            print("✅ Admin créé: admin@babi.com / admin123")
        else:
            print("ℹ️ Admin existe déjà: admin@babi.com")
        
        try:
            db.session.commit()
            print("\n🎉 Utilisateurs de test créés avec succès!")
            print("\n📋 Identifiants de connexion:")
            print("👤 Client: test@babi.com / password123")
            print("🏪 Partenaire: partenaire@babi.com / partner123") 
            print("👨‍💼 Admin: admin@babi.com / admin123")
            
        except Exception as e:
            db.session.rollback()
            print(f"❌ Erreur lors de la création: {e}")

if __name__ == '__main__':
    seed_test_users()

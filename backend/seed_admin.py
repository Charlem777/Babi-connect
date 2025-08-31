# seed_admin.py

from backend.models import db, Utilisateur
from werkzeug.security import generate_password_hash

def seed_admin():
    admin = Utilisateur(
        nom='Admin',
        prenom='Super',
        email='admin@example.com',
        type_utilisateur='Admin',
        mot_de_passe=generate_password_hash('motdepasse123')
    )
    db.session.add(admin)
    db.session.commit()

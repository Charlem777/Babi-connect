# scripts/seed_secteurs.py (par ex.)
from backend.extensions import db
from backend.models import Secteur

def seed_secteurs():
    secteurs = [
        Secteur(nom='Événementiel', slug='evenementiel', description='Organisation d’événements, mariages, séminaires'),
        Secteur(nom='Restauration', slug='restauration', description='Maquis, restaurants, traiteurs'),
        Secteur(nom='Beauté & Esthétique', slug='beaute-esthetique', description='Coiffure, maquillage, soins'),
        Secteur(nom='Formation & Éducation', slug='formation-education', description='Cours, écoles, formations'),
        Secteur(nom='Transport & Logistique', slug='transport-logistique', description='Livraison, taxi, déménagement'),
        Secteur(nom='Technologie', slug='technologie', description='Services numériques, réparation, développement'),
        Secteur(nom='Artisanat & Création', slug='artisanat-creation', description='Couture, menuiserie, design local')
    ]
    db.session.add_all(secteurs)
    db.session.commit()
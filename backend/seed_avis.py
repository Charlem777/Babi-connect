# seed_avis.py
from app import db
from models import AvisPartenaire
from datetime import datetime, timedelta

def seed_avis_partenaire():
    avis_data = [
        {
            "utilisateur_id": 1,
            "partenaire_id": 2,
            "commentaire": "Service impeccable, ambiance chaleureuse. Le tajine était divin.",
            "note": 4.8,
            "date_avis": datetime.utcnow() - timedelta(days=3)
        },
        {
            "utilisateur_id": 2,
            "partenaire_id": 1,
            "commentaire": "Bonne expérience globale, mais un peu bruyant en soirée.",
            "note": 4.2,
            "date_avis": datetime.utcnow() - timedelta(days=7)
        },
        {
            "utilisateur_id": 3,
            "partenaire_id": 3,
            "commentaire": "Accueil froid, plats moyens. Je m’attendais à mieux vu les avis.",
            "note": 2.9,
            "date_avis": datetime.utcnow() - timedelta(days=1)
        },
        {
            "utilisateur_id": 4,
            "partenaire_id": 2,
            "commentaire": "Très bon rapport qualité/prix. Le couscous du vendredi est une tuerie.",
            "note": 4.5,
            "date_avis": datetime.utcnow() - timedelta(days=5)
        },
        {
            "utilisateur_id": 5,
            "partenaire_id": 1,
            "commentaire": "Endroit cosy, parfait pour un déjeuner pro. Wifi stable aussi.",
            "note": 4.7,
            "date_avis": datetime.utcnow() - timedelta(days=2)
        }
    ]

    for data in avis_data:
        avis = AvisPartenaire(**data)
        db.session.add(avis)

    db.session.commit()
    print("✅ Avis partenaires seedés avec succès.")
if __name__ == "__main__":
    seed_avis_partenaire()
avis = AvisPartenaire.query.all()
for a in avis:
    print(f"{a.utilisateur_id} → {a.partenaire_id} : {a.note} ⭐️")

from app import db
from models import Favori
from datetime import datetime, timedelta

def seed_favoris():
    favoris_data = [
        {"utilisateur_id": 1, "offre_id": 1, "date_ajout": datetime.utcnow() - timedelta(days=2)},
        {"utilisateur_id": 2, "offre_id": 2, "date_ajout": datetime.utcnow() - timedelta(days=5)},
        {"utilisateur_id": 3, "offre_id": 3, "date_ajout": datetime.utcnow() - timedelta(days=1)},
        {"utilisateur_id": 4, "offre_id": 1, "date_ajout": datetime.utcnow() - timedelta(days=3)},
        {"utilisateur_id": 5, "offre_id": 2, "date_ajout": datetime.utcnow() - timedelta(days=4)},
    ]

    for data in favoris_data:
        favori = Favori(**data)
        db.session.add(favori)

    try:
        db.session.commit()
        print("✅ Favoris seedés avec succès.")
    except Exception as e:
        db.session.rollback()
        print(f"❌ Erreur lors du seed des favoris : {e}")

if __name__ == "__main__":
    seed_favoris()

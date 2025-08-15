# seed_slugs.py
from app import app, db
from models import Partenaire
import re

def slugify(text):
    text = text.lower()
    text = re.sub(r"[^\w\s-]", "", text)
    text = re.sub(r"[\s_-]+", "-", text)
    return text.strip("-")

with app.app_context():
    partenaires = Partenaire.query.all()
    for p in partenaires:
        if not p.slug:
            p.slug = slugify(p.nom)
            print(f"✅ Slug ajouté pour {p.nom} → {p.slug}")
    db.session.commit()
    print("🎉 Tous les slugs ont été injectés.")

from flask.cli import with_appcontext
import click
from backend.extensions import db
from backend.models import Partenaire, Tag
import re

def slugify(text):
    text = text.lower()
    text = re.sub(r"[^\w\s-]", "", text)
    text = re.sub(r"[\s_-]+", "-", text)
    return text.strip("-")

@click.command("seed_slugs")
@with_appcontext
def seed_slugs():
    partenaires = Partenaire.query.all()
    for p in partenaires:
        if not p.url:
            p.url = slugify(p.nom)
            print(f"✅ Slug ajouté pour {p.nom} → {p.url}")
    db.session.commit()
    print("🎉 Slugs injectés avec succès.")

@click.command("seed-tags")
@with_appcontext
def seed_tags():
    tags = [
        "Service à domicile",
        "Urgence",
        "Garantie 30 jours",
        "Paiement mobile",
        "Disponible le week-end",
        "Travail soigné",
        "Promo",
        "Installation incluse",
        "Réservation en ligne",
        "Livraison express",
        "Disponible en soirée",
        "Éco-responsable",
        "Premium",
        "Disponible à Yopougon",
        "Disponible à Cocody",
        "Disponible à Marcory",
        "Disponible à Treichville",
        "Disponible à Abobo",
        "Disponible à Plateau"
    ]

    ajoutés = 0
    for nom in tags:
        if not Tag.query.filter_by(nom=nom).first():
            db.session.add(Tag(nom=nom))
            ajoutés += 1

    db.session.commit()
    print(f"✅ {ajoutés} tags ajoutés avec succès.")

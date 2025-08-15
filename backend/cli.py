from flask.cli import with_appcontext
import click
from backend.extensions import db
from backend.models import Partenaire
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

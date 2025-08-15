# backend/routes/offres.py (exemple)
from flask import Blueprint, jsonify, request
from backend.models import Offre, Secteur, CategoriePartenaire, Partenaire
from backend.extensions import db

offres_bp = Blueprint("offres", __name__)

@offres_bp.get("/offres")
def list_offres():
    q = Offre.query.join(Partenaire)

    secteur_slug = request.args.get("secteur_slug")
    if secteur_slug:
        q = q.join(Secteur).filter(Secteur.slug == secteur_slug)

    categorie_slug = request.args.get("categorie_slug")
    if categorie_slug:
        q = q.join(CategoriePartenaire).filter(CategoriePartenaire.slug == categorie_slug)

    offres = q.order_by(Offre.date_publication.desc()).limit(100).all()

    return jsonify([
        {
            "id": o.id,
            "titre": o.titre,
            "prix": o.prix,
            "partenaire": o.partenaire.nom,
            "secteur": o.partenaire.secteur.slug if o.partenaire and o.partenaire.secteur else None,
            "categorie": o.partenaire.categorie_partenaire.slug if o.partenaire and o.partenaire.categorie_partenaire else None,
            "image_banniere": o.image_banniere,
        }
        for o in offres
    ])

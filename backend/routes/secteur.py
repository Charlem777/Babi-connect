# backend/routes/secteur.py
from flask import Blueprint, jsonify, abort, request
from backend.models import Secteur, CategoriePartenaire

secteur_bp = Blueprint("secteur", __name__, url_prefix="/api")

@secteur_bp.get("/secteurs")
def get_secteurs():
    secteurs = Secteur.query.order_by(Secteur.nom.asc()).all()
    return jsonify([
        {"id": s.id, "nom": s.nom, "slug": s.slug, "description": s.description, "image": s.photo}
        for s in secteurs
    ])
@secteur_bp.get("/categories")
def get_all_categories():
    categories = CategoriePartenaire.query.order_by(CategoriePartenaire.nom.asc()).all()
    return jsonify([
        {"id": c.id, "nom": c.nom, "slug": c.slug, "description": c.description}
        for c in categories
    ])

@secteur_bp.get("/secteurs/<slug>/categories")
def get_categories_by_secteur(slug):
    secteur = Secteur.query.filter_by(slug=slug).first()
    if not secteur:
        abort(404, description="Secteur introuvable")
    categories = secteur.categories_partenaire  # relation back_populates
    return jsonify([
        {"id": c.id, "nom": c.nom, "slug": c.slug, "description": c.description}
        for c in categories
    ])

from flask import Blueprint, jsonify, request
from backend.models import CategoriePartenaire, CategorieOffre  
categorie_bp = Blueprint('categorie', __name__)

# Exemple : Liste toutes les catégories de partenaires
@categorie_bp.route('/partenaires', methods=['GET'])
def get_categories_partenaires():
    categories = CategoriePartenaire.query.all()
    return jsonify([{"id": c.id, "nom": c.nom, "description": c.description} for c in categories])

# Exemple : Liste toutes les catégories d'offres
@categorie_bp.route('/offres', methods=['GET'])
def get_categories_offres():
    categories = CategorieOffre.query.all()
    return jsonify([{"id": c.id, "nom": c.nom, "description": c.description} for c in categories])
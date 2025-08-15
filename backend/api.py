from flask import Blueprint, jsonify
from backend.models import Partenaire  # si tu as un modèle ORM

api_bp = Blueprint('api', __name__, url_prefix='/api')

@api_bp.route('/partenaires', methods=['GET'])
def get_partenaires():
    partenaires = Partenaire.query.all()
    results = [
        {
            "id": p.id,
            "nom": p.nom,
            "secteur": p.secteur,
            "commune": p.commune,
            "logo": p.logo,
            "description": p.description,
            "note_moyenne": p.note_moyenne
        }
        for p in partenaires
    ]
    return jsonify(results)

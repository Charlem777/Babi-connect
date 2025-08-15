from flask import Blueprint, jsonify
from backend.models import Utilisateur

utilisateur_bp = Blueprint('utilisateurs', __name__)

@utilisateur_bp.route('/', methods=['GET'])
def get_utilisateurs():
    utilisateurs = Utilisateur.query.all()
    resultats = []
    for u in utilisateurs:
        resultats.append({
            "id": u.id,
            "nom": u.nom,
            "email": u.email,
            "budget": u.budget,
            "localisation": u.localisation
        })
    return jsonify(resultats)

from flask import Blueprint, request, jsonify
from backend.extensions import db
from backend.models import Abonnement

abonnement_bp = Blueprint('abonnement_bp', __name__)

# 🆕 Ajouter un abonnement
@abonnement_bp.route('/abonnements', methods=['POST'])
def creer_abonnement():
    data = request.json
    nouvel_abonnement = Abonnement(
        partenaire_id=data['partenaire_id'],
        type_abonnement=data['type_abonnement'],
        prix=data['prix'],
        date_fin=data.get('date_fin')
    )
    db.session.add(nouvel_abonnement)
    db.session.commit()
    return jsonify({"message": "Abonnement créé avec succès"}), 201

# 📄 Récupérer tous les abonnements
@abonnement_bp.route('/abonnements', methods=['GET'])
def liste_abonnements():
    abonnements = Abonnement.query.all()
    resultats = [{
        "id": a.id,
        "type": a.type_abonnement,
        "prix": a.prix,
        "partenaire_id": a.partenaire_id,
        "date_debut": a.date_debut,
        "date_fin": a.date_fin,
        "actif": a.actif
    } for a in abonnements]
    return jsonify(resultats), 200

# 🚫 Supprimer un abonnement
@abonnement_bp.route('/abonnements/<int:id>', methods=['DELETE'])
def supprimer_abonnement(id):
    abonnement = Abonnement.query.get_or_404(id)
    db.session.delete(abonnement)
    db.session.commit()
    return jsonify({"message": "Abonnement supprimé"}), 200

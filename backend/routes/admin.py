import datetime
from flask import Blueprint, jsonify, request
from backend.models import (
    Abonnement, CategoriePartenaire, Utilisateur, Partenaire, Offre,
    Secteur, CategorieOffre, db
)
from backend.middlewares.auth import require_auth
import os
from werkzeug.utils import secure_filename
from flask import current_app
from datetime import datetime
admin_bp = Blueprint('admin', __name__, url_prefix='/api/admin')

def generate_slug(nom):
    return nom.lower().strip().replace(' ', '-')

# ============================
# 📊 Statistiques Dashboard
# ============================
@admin_bp.route('/stats', methods=['GET'])
@require_auth(role='admin')
def get_admin_stats():
    return jsonify({
        "utilisateurs": Utilisateur.query.count(),
        "partenaires": Partenaire.query.count(),
        "offres": Offre.query.count(),
        "secteurs": Secteur.query.count(),
        "categories": CategorieOffre.query.count(),
        "abonnements": Abonnement.query.count()

    })

# ============================
# 🎁 Offres récentes
# ============================
@admin_bp.route('/offres/recentes', methods=['GET'])
@require_auth(role='admin')
def offres_recentes():
    offres = Offre.query.order_by(Offre.date_publication.desc()).limit(5).all()
    return jsonify([o.to_dict() for o in offres])

# ============================
# 🤝 Partenaires récents
# ============================
@admin_bp.route('/partenaires/recent', methods=['GET', 'OPTIONS'])
@require_auth(role='admin')
def partenaires_recents():
    partenaires = Partenaire.query.order_by(Partenaire.date_inscription.desc()).limit(5).all()
    return jsonify([p.to_dict() for p in partenaires])

# ============================
# 🏷️ Secteurs
# ============================
@admin_bp.route('/secteurs', methods=['GET'])
@require_auth(role='admin')
def get_secteurs():

    secteurs = Secteur.query.order_by(Secteur.nom.asc()).all()
    return jsonify([s.to_dict() for s in secteurs])

@admin_bp.route('/secteurs/<int:id>', methods=['GET'])
@require_auth(role='admin')
def get_secteur(id):
    secteur = Secteur.query.get_or_404(id)
    return jsonify(secteur.to_dict())

@admin_bp.route('/secteurs', methods=['POST'])
@require_auth(role='admin')
def create_secteur():
    data = request.get_json()
    nom = data.get('nom')
    slug = data.get('slug')
    description = data.get('description', '')
    photo = data.get('photo', '')

    if not nom or not slug:
        return jsonify({"error": "Champs requis"}), 400

    if Secteur.query.filter_by(nom=nom).first():
        return jsonify({"error": "Nom déjà utilisé"}), 409
    if Secteur.query.filter_by(slug=slug).first():
        return jsonify({"error": "Slug déjà utilisé"}), 409
    
    secteur = Secteur(nom=nom, slug=slug, description=description, photo=photo)
    db.session.add(secteur)
    db.session.commit()
    return jsonify(secteur.to_dict()), 201


@admin_bp.route('/secteurs/<int:id>', methods=['PUT'])
@require_auth(role='admin')
def update_secteur(id):
    secteur = Secteur.query.get_or_404(id)
    data = request.get_json()

    nom = data.get('nom')
    slug = data.get('slug')
    description = data.get('description', secteur.description)
    photo = data.get('photo', secteur.photo)

    if not nom or not slug:
        return jsonify({"error": "Nom et slug requis"}), 400

    secteur.nom = nom
    secteur.slug = slug
    secteur.description = description
    secteur.photo = photo  # ← cette ligne manquait

    db.session.commit()
    return jsonify(secteur.to_dict())
@admin_bp.route('/secteurs/<int:id>', methods=['DELETE', 'OPTIONS'])
@require_auth(role='admin')
def delete_secteur(id):
    if request.method == 'OPTIONS':
        return '', 200

    secteur = Secteur.query.get_or_404(id)

    if secteur.partenaires and len(secteur.partenaires) > 0:
        return jsonify({
            "error": "Ce secteur est associé à des partenaires",
            "partenaires": len(secteur.partenaires)
        }), 400

    if secteur.categories_partenaire and len(secteur.categories_partenaire) > 0:
        return jsonify({
            "error": "Ce secteur est associé à des catégories partenaires",
            "categories": len(secteur.categories_partenaire)
        }), 400

    db.session.delete(secteur)
    db.session.commit()
    return jsonify({"message": "Secteur supprimé"}), 200

import os
from flask import current_app, url_for, request, jsonify
from werkzeug.utils import secure_filename
import os

@admin_bp.route('/upload/secteur-photo', methods=['POST', 'OPTIONS'])
@require_auth(role='admin')
def upload_secteur_photo():
    if request.method == 'OPTIONS':
        return '', 200
    if not request.files or 'photo' not in request.files:
        return jsonify({"error": "Aucun fichier reçu"}), 400

    file = request.files['photo']
    if file.filename == '':
        return jsonify({"error": "Nom de fichier vide"}), 400

    filename = secure_filename(file.filename)
    upload_path = os.path.join(current_app.root_path, 'static', 'uploads', 'secteurs')
    os.makedirs(upload_path, exist_ok=True)
    file_path = os.path.join(upload_path, filename)
    file.save(file_path)

    photo_url = url_for('static', filename=f'uploads/secteurs/{filename}', _external=True)
    return jsonify({"url": photo_url})

# ============================
# 📂 Catégories partenaires
# ============================
@admin_bp.route('/categories-partenaires', methods=['GET'])
@require_auth(role='admin')
def get_categories():
    categories = CategoriePartenaire.query.order_by(CategoriePartenaire.nom.asc()).all()
    return jsonify([c.to_dict() for c in categories])

@admin_bp.route('/categories-partenaires', methods=['POST'])
@require_auth(role='admin')
def create_categorie():
    data = request.get_json()
    nom = data.get('nom')
    description = data.get('description', '')
    secteur_id = data.get('secteur_id')

    if not nom or not secteur_id:
        return jsonify({"error": "Nom et secteur requis"}), 400

    if CategoriePartenaire.query.filter_by(nom=nom).first():
        return jsonify({"error": "Nom déjà utilisé"}), 409

    secteur = Secteur.query.get(secteur_id)
    if not secteur:
        return jsonify({"error": "Secteur introuvable"}), 404

    slug = generate_slug(nom)

    cat = CategoriePartenaire(nom=nom, slug=slug, description=description, secteur=secteur)
    db.session.add(cat)
    db.session.commit()
    return jsonify(cat.to_dict()), 201



@admin_bp.route('/categories-partenaires/<int:id>', methods=['PUT'])
@require_auth(role='admin')
def update_categorie(id):
    cat = CategoriePartenaire.query.get_or_404(id)
    data = request.get_json()

    nom = data.get('nom')
    description = data.get('description', cat.description)
    secteur_id = data.get('secteur_id', cat.secteur_id)

    if not nom or not secteur_id:
        return jsonify({"error": "Nom et secteur requis"}), 400

    secteur = Secteur.query.get(secteur_id)
    if not secteur:
        return jsonify({"error": "Secteur introuvable"}), 404

    slug = generate_slug(nom)

    cat.nom = nom
    cat.slug = slug
    cat.description = description
    cat.secteur = secteur

    db.session.commit()
    return jsonify(cat.to_dict())



@admin_bp.route('/categories-partenaires/<int:id>', methods=['DELETE'])
@require_auth(role='admin')
def delete_categorie(id):
    if request.method == 'OPTIONS':
        return '', 200
    cat = CategoriePartenaire.query.get_or_404(id)

    if cat.partenaires and len(cat.partenaires) > 0:
        return jsonify({
            "error": "Cette catégorie est associée à des partenaires",
            "partenaires": len(cat.partenaires)
        }), 400

    db.session.delete(cat)
    db.session.commit()
    return jsonify({"message": "Catégorie supprimée"}), 200

@admin_bp.route('/partenaires/<int:id>', methods=['GET', 'OPTIONS'])
@require_auth(role='admin')
def get_partenaires_abonnement(id):
    if request.method == 'OPTIONS':
        return '', 200  # Réponse préflight OK

    partenaires = Partenaire.query.get_or_404(id)
    print(partenaires)
    return jsonify(partenaires.to_dict())

@admin_bp.route('/partenaires', methods=['GET', 'OPTIONS'])
@require_auth(role='admin')
def get_partenaires_admin():
    if request.method == 'OPTIONS':
        return '', 200  # Réponse préflight OK

    partenaires = Partenaire.query.all()
    result = [p.to_dict() for p in partenaires]
    return jsonify(result)

@admin_bp.route('/abonnements', methods=['POST'])
@require_auth(role='admin')
def create_abonnement():
    data = request.get_json()
    partenaire_id = data.get('partenaire_id')
    type = data.get('type')
    date_fin = data.get('date_fin')

    if not partenaire_id or not type:
        return jsonify({"error": "Partenaire et type requis"}), 400

    # désactiver l’ancien abonnement s’il existe
    Abonnement.query.filter_by(partenaire_id=partenaire_id, actif=True).update({"actif": False})

    abonnement = Abonnement(
        partenaire_id=partenaire_id,
        type=type,
        date_fin=datetime.fromisoformat(date_fin) if date_fin else None,
        actif=True
    )
    db.session.add(abonnement)
    db.session.commit()
    return jsonify({"message": "Abonnement créé"})

from datetime import datetime

@admin_bp.route('/abonnements/<int:id>', methods=['PUT'])
@require_auth(role='admin')
def update_abonnement(id):
    if request.method == 'OPTIONS':
        return '', 200  # Réponse préflight OK

    ab = Abonnement.query.get_or_404(id)
    data = request.get_json() or {}
    print(" reçu :", data)

    # Mise à jour du type (si nécessaire valider les valeurs)
    if 'type' in data and data['type'] is not None:
        ab.type = data['type']

    # Helper pour parser une date (accepte YYYY-MM-DD ou ISO). Retourne None si vide.
    def parse_date_maybe(date_str, field_name):
        if date_str is None or (isinstance(date_str, str) and date_str.strip() == ""):
            return None
        # try ISO first
        try:
            return datetime.fromisoformat(date_str)
        except Exception:
            pass
        # try date-only format YYYY-MM-DD
        try:
            return datetime.strptime(date_str.split('T')[0], "%Y-%m-%d")
        except Exception:
            raise ValueError(f"Format de {field_name} invalide")

    # date_debut
    if 'date_debut' in data:
        try:
            parsed = parse_date_maybe(data.get('date_debut'), 'date_debut')
            ab.date_debut = parsed
        except ValueError as e:
            return jsonify({"error": str(e)}), 400

    # date_fin
    if 'date_fin' in data:
        try:
            parsed = parse_date_maybe(data.get('date_fin'), 'date_fin')
            ab.date_fin = parsed
        except ValueError as e:
            return jsonify({"error": str(e)}), 400

    # actif (convertir proprement)
    if 'actif' in data:
        val = data.get('actif')
        if isinstance(val, bool):
            ab.actif = val
        else:
            # accepter "true"/"false"/"1"/"0"
            ab.actif = str(val).lower() in ("true", "1", "yes")

    db.session.commit()
    return jsonify({"message": "Abonnement mis à jour"})




@admin_bp.route('/partenaires/<int:id>/abonnements', methods=['GET'])
@require_auth(role='admin')
def historique_abonnements(id):
    abonnements = Abonnement.query.filter_by(partenaire_id=id).order_by(Abonnement.date_debut.desc()).all()
    return jsonify([
        {
            "id": ab.id,
            "type": ab.type,
            "date_debut": ab.date_debut.isoformat(),
            "date_fin": ab.date_fin.isoformat() if ab.date_fin else None,
            "actif": ab.actif
        } for ab in abonnements
    ])

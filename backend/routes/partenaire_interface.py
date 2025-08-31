# backend/routes/partenaire_interface.py

import os
from flask import Blueprint, request, jsonify, g
from backend.extensions import db
from backend.models import CategorieOffre, OffrePhoto, OffreTag, Partenaire, Offre, Abonnement, AvisPartenaire, CommentaireOffre, OffreOption, Tag
from backend.middlewares.auth import require_auth
from datetime import datetime
from werkzeug.utils import secure_filename

partenaireint_bp = Blueprint('partenaireint', __name__)

# 🔐 Récupérer le profil du partenaire connecté
@partenaireint_bp.route('/me', methods=['GET', 'OPTIONS'])
@require_auth(role='partenaire')
def get_mon_profil():
    if request.method == 'OPTIONS':
        return '', 200
    print("🔍 g.user =", g.user)
    print("🔍 Type de g.user =", type(g.user))

    return jsonify(g.user.to_dict())

# 🖼️ Modifier le profil
@partenaireint_bp.route('/me', methods=['PUT'])
@require_auth(role='partenaire')
def update_mon_profil():
    if request.method == 'OPTIONS':
        return '', 200
    data = request.get_json()
    partenaire = Partenaire.query.get_or_404(g.user.id)

    for field in ['nom', 'description', 'ville', 'commune', 'localisation', 'logo', 'url', 'reseaux']:
        if field in data:
            setattr(partenaire, field, data[field])

    db.session.commit()
    return jsonify({"message": "Profil mis à jour"})

# 💼 Voir l’abonnement
@partenaireint_bp.route('/abonnement', methods=['GET', 'OPTIONS'])
@require_auth(role='partenaire')
def get_abonnement():
    if request.method == 'OPTIONS':
        return '', 200
    partenaire = Partenaire.query.get_or_404(g.user.id)
    ab = partenaire.abonnement
    if not ab:
        return jsonify(None)
    return jsonify({
        "id": ab.id,
        "type": ab.type,
        "date_debut": ab.date_debut.isoformat(),
        "date_fin": ab.date_fin.isoformat() if ab.date_fin else None,
        "actif": ab.actif
    })
@require_auth(role='partenaire')
@partenaireint_bp.route('/tags', methods=['GET'])
def get_tags():
    tags = Tag.query.order_by(Tag.nom).all()
    return jsonify([{'id': t.id, 'nom': t.nom} for t in tags])

# 🎯 Liste des offres du partenaire
@partenaireint_bp.route('/offres', methods=['GET'])
@require_auth(role='partenaire')
def get_mes_offres():
    partenaire_id = g.user.id
    offres = Offre.query.filter_by(partenaire_id=partenaire_id).order_by(Offre.date_publication.desc()).all()
    return jsonify([o.to_dict() for o in offres])

from datetime import datetime

# 🔍 Récupérer les catégories
@partenaireint_bp.route('/categories-offres', methods=['GET'])
@require_auth(role='partenaire')
def get_categories_offres():
    categories = CategorieOffre.query.order_by(CategorieOffre.nom.asc()).all()
    return jsonify([{
        "id": c.id,
        "nom": c.nom,
        "slug": c.slug,
        "description": c.description
    } for c in categories])

# 🆕 Créer une offre
@partenaireint_bp.route('/offres', methods=['POST'])
@require_auth(role='partenaire')
def create_offre():
    data = request.get_json()
    print("📦 Payload reçu :", request.get_json())
    print("👤 Partenaire ID i :", g.user.id)

    try:
        expire_le = None
        if data.get('expire_le'):
            expire_le = datetime.strptime(data['expire_le'], "%Y-%m-%d")

        offre = Offre(
            titre=data.get('titre'),
            description=data.get('description'),
            prix=data.get('prix'),
            ville=data.get('ville'),
            commune=data.get('commune'),
            localisation=data.get('localisation'),
            expire_le=expire_le,
            image_banniere=data.get('image_banniere'),
            categorie_offre_id=data.get('categorie_offre_id'),
            partenaire_id=g.user.id

        )

        # Tags
        for tag_id in data.get('tags', []):
            tag = Tag.query.get(tag_id)
            if tag:
                offre.offre_tags.append(OffreTag(tag=tag))

        # Options
        for opt in data.get('options', []):
            if opt.get('nom'):
                offre.options.append(OffreOption(
                    nom=opt['nom'],
                    valeur=opt.get('valeur'),
                    prix_supplementaire=opt.get('prix_supplementaire', 0.0)
                ))

        # Photos
        for url in data.get('photos', []):
            if url:
                offre.photos.append(OffrePhoto(url=url))

        db.session.add(offre)
        db.session.commit()
        db.session.refresh(offre)
        return jsonify({
            'message': 'Offre créée avec succès',
            'offre': offre.to_dict()
        }), 201

    except Exception as e:
        db.session.rollback()
        print("❌ Erreur lors de la création d’offre :", str(e))  # ← log utile
        
        return jsonify({'error': str(e)}), 400


from flask import current_app
import os
from werkzeug.utils import secure_filename

@partenaireint_bp.route('/upload/logo-partenaire', methods=['POST'])
@require_auth(role='partenaire')
def upload_logo():
    file = request.files.get('image')
    if not file:
        return jsonify({'error': 'Aucun fichier reçu'}), 400

    # 📂 Chemin absolu vers static/uploads
    upload_dir = os.path.join(current_app.root_path, 'static', 'uploads')
    os.makedirs(upload_dir, exist_ok=True)

    filename = secure_filename(file.filename)
    path = os.path.join(upload_dir, filename)
    file.save(path)

    # URL publique pour accéder au fichier
    url = f'/static/uploads/{filename}'
    return jsonify({'url': url})

@partenaireint_bp.route('/upload/photo-offre', methods=['POST'])
def upload_photo():
    file = request.files.get('image')
    if not file:
        return jsonify({'error': 'Aucun fichier reçu'}), 400

    # 📂 Chemin absolu vers static/uploads
    upload_dir = os.path.join(current_app.root_path, 'static', 'uploads')
    os.makedirs(upload_dir, exist_ok=True)  # ✅ crée le dossier si absent

    filename = secure_filename(file.filename)
    path = os.path.join(upload_dir, filename)
    file.save(path)

    # URL publique pour accéder au fichier
    url = f'/static/uploads/{filename}'
    return jsonify({'url': url})

    file = request.files.get('image')
    if not file:
        return jsonify({'error': 'Aucun fichier reçu'}), 400

    filename = secure_filename(file.filename)
    path = os.path.join('static/uploads', filename)
    file.save(path)

    url = f'/static/uploads/{filename}'
    return jsonify({'url': url})

    # 🔍 Récupérer une offre spécifique
@partenaireint_bp.route('/offres/<int:id>', methods=['GET'])
@require_auth(role='partenaire')
def get_offre(id):
    offre = Offre.query.filter_by(id=id, partenaire_id=g.user.id).first_or_404()
    return jsonify(offre.to_dict())

# ✏️ Modifier une offre
@partenaireint_bp.route('/offres/<int:id>', methods=['PUT'])
@require_auth(role='partenaire')
def update_offre(id):
    data = request.get_json()
    offre = Offre.query.filter_by(id=id, partenaire_id=g.user.id).first_or_404()

    # Mettre à jour les champs de base
    for field in ['titre', 'description', 'prix', 'ville', 'commune', 'image_banniere', 'localisation', 'categorie_offre_id']:
        if field in data:
            setattr(offre, field, data[field])

    # Mettre à jour la date d'expiration
    if 'expire_le' in data and data['expire_le']:
        offre.expire_le = datetime.strptime(data['expire_le'], "%Y-%m-%d")

    # Supprimer les anciennes options
    for option in offre.options:
        db.session.delete(option)
    
    # Ajouter les nouvelles options
    for opt in data.get('options', []):
        if opt.get('nom'):
            offre.options.append(OffreOption(
                nom=opt['nom'],
                valeur=opt.get('valeur'),
                prix_supplementaire=opt.get('prix_supplementaire', 0.0)
            ))

    # Supprimer les anciens tags
    for offre_tag in offre.offre_tags:
        db.session.delete(offre_tag)
    
    # Ajouter les nouveaux tags
    for tag_id in data.get('tags', []):
        tag = Tag.query.get(tag_id)
        if tag:
            offre.offre_tags.append(OffreTag(tag=tag))

    # Supprimer les anciennes photos
    for photo in offre.photos:
        db.session.delete(photo)
    
    # Ajouter les nouvelles photos
    for url in data.get('photos', []):
        if url:
            offre.photos.append(OffrePhoto(url=url))

    db.session.commit()
    return jsonify({"message": "Offre mise à jour avec succès"})

# 🗑️ Supprimer une offre
@partenaireint_bp.route('/offres/<int:id>', methods=['DELETE'])
@require_auth(role='partenaire')
def delete_offre(id):
    offre = Offre.query.filter_by(id=id, partenaire_id=g.user.id).first_or_404()
    db.session.delete(offre)
    db.session.commit()
    return jsonify({"message": "Offre supprimée"})

# 📊 Statistiques globales
@partenaireint_bp.route('/stats', methods=['GET'])
@require_auth(role='partenaire')
def get_stats():
    partenaire_id = partenaire_id = g.user.id  
    offres = Offre.query.filter_by(partenaire_id=partenaire_id).all()
    total_vues = sum(o.vues for o in offres)
    total_clics = sum(o.clics for o in offres)
    total_favoris = sum(o.favoris_count for o in offres)
    return jsonify({
        "vues": total_vues,
        "clics": total_clics,
        "favoris": total_favoris,
        "offres": len(offres)
    })

# 💬 Avis reçus
@partenaireint_bp.route('/avis', methods=['GET'])
@require_auth(role='partenaire')
def get_avis():
    avis = AvisPartenaire.query.filter_by(partenaire_id=g.user.id).order_by(AvisPartenaire.date.desc()).all()
    return jsonify([{
        "id": a.id,
        "note": a.note,
        "commentaire": a.commentaire,
        "date": a.date.isoformat()
    } for a in avis])

# 💬 Récupérer les commentaires des offres du partenaire
@partenaireint_bp.route('/commentaires', methods=['GET'])
@require_auth(role='partenaire')
def get_commentaires():
    # Récupérer toutes les offres du partenaire
    offres = Offre.query.filter_by(partenaire_id=g.user.id).all()
    offre_ids = [offre.id for offre in offres]
    
    # Récupérer tous les commentaires de ces offres
    commentaires = CommentaireOffre.query.filter(CommentaireOffre.offre_id.in_(offre_ids)).order_by(CommentaireOffre.date.desc()).all()
    
    result = []
    for commentaire in commentaires:
        result.append({
            "id": commentaire.id,
            "commentaire": commentaire.commentaire,
            "date": commentaire.date.isoformat() if commentaire.date else None,
            "utilisateur": {
                "id": commentaire.utilisateur.id,
                "nom": commentaire.utilisateur.nom,
                "prenom": commentaire.utilisateur.prenom
            } if commentaire.utilisateur else None,
            "offre": {
                "id": commentaire.offre.id,
                "titre": commentaire.offre.titre
            },
            "reponses": commentaire.reponses or []
        })
    
    return jsonify(result)

# 💬 Répondre à un commentaire
@partenaireint_bp.route('/commentaires/<int:commentaire_id>/repondre', methods=['POST'])
@require_auth(role='partenaire')
def repondre_commentaire(commentaire_id):
    data = request.get_json()
    reponse_text = data.get('reponse')
    
    if not reponse_text:
        return jsonify({"error": "La réponse ne peut pas être vide"}), 400
    
    # Vérifier que le commentaire appartient à une offre du partenaire
    commentaire = CommentaireOffre.query.join(Offre).filter(
        CommentaireOffre.id == commentaire_id,
        Offre.partenaire_id == g.user.id
    ).first_or_404()
    
    # Ajouter la réponse
    if not commentaire.reponses:
        commentaire.reponses = []
    
    nouvelle_reponse = {
        "id": len(commentaire.reponses) + 1,
        "reponse": reponse_text,
        "date": datetime.utcnow().isoformat(),
        "partenaire": {
            "id": g.user.id,
            "nom": g.user.nom
        }
    }
    
    commentaire.reponses.append(nouvelle_reponse)
    db.session.commit()
    
    return jsonify({"message": "Réponse ajoutée avec succès", "reponse": nouvelle_reponse})

@partenaireint_bp.route('/debug-user', methods=['GET'])
@require_auth(role='partenaire')
def debug_user():
    return jsonify({
        "type": str(type(g.user)),
        "id": g.user.id,
        "nom": g.user.nom
    })

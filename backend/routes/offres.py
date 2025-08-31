from flask import Blueprint, request, jsonify, g
from backend.models import Offre, Partenaire, Secteur, CategorieOffre, CommentaireOffre, FavoriOffre, CategoriePartenaire, Abonnement
from backend.extensions import db
from backend.middlewares.auth import require_auth, optional_auth
from datetime import datetime
from sqlalchemy import func, or_
from urllib.parse import unquote

offres_bp = Blueprint("offres", __name__)

# Liste des offres avec filtres dynamiques
@offres_bp.route("/offres")
def list_offres():
    # Temporarily remove subscription enforcement for debugging
    q = Offre.query.join(Partenaire)
    print(f" Base query count: {q.count()}")

    # Filtres existants
    secteur_slug = request.args.get("secteur_slug")
    if secteur_slug:
        secteur_slug = unquote(secteur_slug)
        q = q.join(Secteur).filter(Secteur.slug == secteur_slug)
        print(f"After secteur filter: {q.count()}")

    categorie_slug = request.args.get("categorie_slug")
    if categorie_slug:
        categorie_slug = unquote(categorie_slug)
        q = q.join(CategoriePartenaire).filter(CategoriePartenaire.slug == categorie_slug)
        print(f"After categorie filter: {q.count()}")

    # Nouveaux filtres géolocalisés
    ville = request.args.get("ville")
    if ville:
        ville = unquote(ville)
        q = q.filter(Offre.ville.ilike(f"%{ville}%"))
        print(f"After ville filter ({ville}): {q.count()}")

    commune = request.args.get("commune")
    if commune:
        commune = unquote(commune)
        q = q.filter(Offre.commune.ilike(f"%{commune}%"))
        print(f"After commune filter ({commune}): {q.count()}")

    # Filtres de budget
    prix_min = request.args.get("prix_min")
    if prix_min:
        try:
            prix_min = float(prix_min)
            q = q.filter(Offre.prix >= prix_min)
            print(f"After prix_min filter: {q.count()}")
        except ValueError:
            pass

    prix_max = request.args.get("prix_max")
    if prix_max:
        try:
            prix_max = float(prix_max)
            q = q.filter(Offre.prix <= prix_max)
            print(f"After prix_max filter: {q.count()}")
        except ValueError:
            pass

    # Tri
    sort_by = request.args.get("sort", "recent")
    if sort_by == "price_asc":
        q = q.order_by(Offre.prix.asc())
    elif sort_by == "price_desc":
        q = q.order_by(Offre.prix.desc())
    elif sort_by == "popularity":
        q = q.order_by(Offre.favoris_count.desc())
    else:  # recent par défaut
        q = q.order_by(Offre.date_publication.desc())

    # Pagination
    page = request.args.get("page", 1, type=int)
    per_page = request.args.get("per_page", 20, type=int)
    
    offres = q.limit(per_page).offset((page - 1) * per_page).all()
    total = q.count()
    
    print(f"Final offres count: {len(offres)}")
    print(f"Request params: {dict(request.args)}")

    return jsonify({
        "offres": [
            {
                "id": o.id,
                "titre": o.titre,
                "description": o.description,
                "prix": o.prix,
                "ville": o.ville,
                "commune": o.commune,
                "secteur": o.partenaire.secteur.nom if o.partenaire.secteur else None,
                "partenaire": {
                    "id": o.partenaire.id,
                    "nom": o.partenaire.nom,
                    "logo": o.partenaire.logo,
                    "secteur": o.partenaire.secteur.slug if o.partenaire.secteur else None,
                    "categorie": o.partenaire.categorie_partenaire.slug if o.partenaire.categorie_partenaire else None
                },
                "image_banniere": o.image_banniere,
                "favoris_count": len(o.favoris),
                "vues": o.vues or 0,
                "date_publication": o.date_publication.isoformat() if o.date_publication else None
            }
            for o in offres
        ],
        "pagination": {
            "page": page,
            "per_page": per_page,
            "total": total,
            "pages": (total + per_page - 1) // per_page
        }
    })

# Détail d’une offre
@offres_bp.route("/offres/<int:id>", methods=["GET"])
def get_offre_detail(id):
    offre = Offre.query.get_or_404(id)
    
    # Incrémenter le compteur de vues
    offre.vues = (offre.vues or 0) + 1
    db.session.commit()
    
    return {
        "id": offre.id,
        "titre": offre.titre,
        "description": offre.description,
        "prix": offre.prix,
        "image_banniere": offre.image_banniere,
        "localisation": offre.localisation,
        "ville": offre.ville,
        "commune": offre.commune,
        "favoris_count": len(offre.favoris),
        "photos": [photo.url for photo in offre.photos],
        "options": [
            {
                "nom": opt.nom,
                "valeur": opt.valeur,
                "prix_supplementaire": opt.prix_supplementaire
            } for opt in offre.options
        ],
        "tags": [tag.tag.nom for tag in offre.offre_tags],
        "partenaire": {
            "id": offre.partenaire.id,
            "nom": offre.partenaire.nom,
            "secteur": offre.partenaire.secteur.nom,
            "secteur_slug": offre.partenaire.secteur.slug,
            "ville": offre.partenaire.ville,
            "url": offre.partenaire.url,
            "commune": offre.partenaire.commune,
            "localisation": offre.partenaire.localisation,
            "description": offre.partenaire.description,
            "note": offre.partenaire.note_moyenne,
            "logo": offre.partenaire.logo,
            "photos": offre.partenaire.photos,
            "abonnement": {
                "type": offre.partenaire.abonnement.type if offre.partenaire.abonnement else None,
                "actif": offre.partenaire.abonnement.actif if offre.partenaire.abonnement else False
            },
            "avis": [
                {
                    "note": avis.note,
                    "commentaire": avis.commentaire,
                    "date": avis.date.isoformat(),
                    "utilisateur": {
                        "nom": avis.utilisateur.nom
                    }
                } for avis in offre.partenaire.avis if avis.visible
            ]
        },
        "commentaires": [
            {
                "id": c.id,
                "commentaire": c.commentaire,
                "date": c.date_creation.isoformat(),
                "utilisateur": {
                    "id": c.utilisateur.id,
                    "nom": c.utilisateur.nom,
                    "prenom": c.utilisateur.prenom
                },
                "parent_id": c.parent_id,
                "reponses": [r.to_dict() for r in c.reponses] if hasattr(c, 'reponses') else []
            } for c in offre.commentaires if c.parent_id is None
        ]
    }

# Offres populaires
@offres_bp.route("/offres/populaires")
def get_offres_populaires():
    try:
        offres = Offre.query.order_by(Offre.favoris_count.desc()).limit(20).all()
        return jsonify([
            {
                "id": o.id,
                "titre": o.titre,
                "prix": o.prix,
                "image_banniere": o.image_banniere,
                "favoris_count": len(o.favoris),
                "partenaire": {
                    "nom": o.partenaire.nom,
                    "commune": o.partenaire.commune,
                    "logo": o.partenaire.logo
                }
            } for o in offres
        ])
    except Exception as e:
        print("Erreur dans /api/offres/populaires :", e)
        return jsonify({"error": "Erreur serveur"}), 500

# Recommandations pour une offre donnée
@offres_bp.route("/offres/<int:id>/recommandations")
def recommandations_offre(id):
    offre = Offre.query.get_or_404(id)

    secteur_slug = offre.partenaire.secteur.slug if offre.partenaire and offre.partenaire.secteur else None
    commune = offre.commune

    recommandations = []
    if secteur_slug and commune:
        recommandations = Offre.query.join(Partenaire).join(Secteur).filter(
            Offre.id != id,
            Secteur.slug == secteur_slug,
            Offre.commune == commune
        ).order_by(Offre.popularite.desc()).limit(6).all()

    # Fallback si trop peu de résultats
    if len(recommandations) < 3:
        autres = Offre.query.filter(Offre.id != id).order_by(Offre.vues.desc()).limit(6).all()
        recommandations += [o for o in autres if o not in recommandations]

    return jsonify([o.to_dict() for o in recommandations])

@offres_bp.route("/search/suggestions")
def search_suggestions():
    q = request.args.get("q", "").strip()
    if not q:
        return jsonify([])

    offres = Offre.query.join(Partenaire).join(Abonnement).filter(
        Abonnement.actif == True,
        Offre.titre.ilike(f"%{q}%")
    ).limit(5).all()
    
    partenaires = Partenaire.query.join(Abonnement).filter(
        Abonnement.actif == True,
        Partenaire.nom.ilike(f"%{q}%")
    ).limit(5).all()
    
    results = [
        {
            "id": o.id, 
            "label": o.titre, 
            "type": "offre",
            "image": o.image_banniere,
            "ville": o.ville,
            "commune": o.commune,
            "secteur": o.partenaire.secteur.slug if o.partenaire.secteur else None
        } for o in offres
    ] + [
        {
            "id": p.id, 
            "slug": p.url, 
            "label": p.nom, 
            "type": "partenaire",
            "image": p.logo,
            "ville": p.ville,
            "commune": p.commune,
            "secteur": p.secteur.slug if p.secteur else None
        } for p in partenaires
    ]

    return jsonify(results)

# Nouveau endpoint pour recherche géolocalisée
@offres_bp.route("/offres/nearby")
def get_nearby_offers():
    ville = request.args.get("ville")
    commune = request.args.get("commune")
    radius_km = request.args.get("radius", 10, type=int)  # Rayon en km
    
    if not ville and not commune:
        return jsonify({"error": "Ville ou commune requise"}), 400

    q = Offre.query.join(Partenaire).join(Abonnement).filter(Abonnement.actif == True)
    
    if ville:
        q = q.filter(Offre.ville.ilike(f"%{ville}%"))
    if commune:
        q = q.filter(Offre.commune.ilike(f"%{commune}%"))

    # Tri par popularité et date
    offres = q.order_by(
        Offre.favoris_count.desc(),
        Offre.date_publication.desc()
    ).limit(20).all()

    return jsonify([
        {
            "id": o.id,
            "titre": o.titre,
            "prix": o.prix,
            "ville": o.ville,
            "commune": o.commune,
            "localisation": o.localisation,
            "image_banniere": o.image_banniere,
            "favoris_count": len(o.favoris),
            "partenaire": {
                "nom": o.partenaire.nom,
                "logo": o.partenaire.logo,
                "note_moyenne": o.partenaire.note_moyenne
            },
            "secteur": o.partenaire.secteur.slug if o.partenaire.secteur else None,
            "distance_approx": "< 5km"  # Placeholder pour future implémentation GPS
        } for o in offres
    ])

# Endpoint pour obtenir les villes/communes populaires
@offres_bp.route("/locations/popular")
def get_popular_locations():
    try:
        # Villes les plus populaires basées sur le nombre d'offres
        villes = db.session.query(
            Offre.ville,
            db.func.count(Offre.id).label('count')
        ).join(Partenaire).join(Abonnement).filter(
            Abonnement.actif == True,
            Offre.ville.isnot(None)
        ).group_by(Offre.ville).order_by(db.func.count(Offre.id).desc()).limit(10).all()

        # Communes les plus populaires
        communes = db.session.query(
            Offre.commune,
            db.func.count(Offre.id).label('count')
        ).join(Partenaire).join(Abonnement).filter(
            Abonnement.actif == True,
            Offre.commune.isnot(None)
        ).group_by(Offre.commune).order_by(db.func.count(Offre.id).desc()).limit(10).all()

        return jsonify({
            "villes": [{"nom": v.ville, "offres_count": v.count} for v in villes],
            "communes": [{"nom": c.commune, "offres_count": c.count} for c in communes]
        })
    except Exception as e:
        print("Erreur dans /api/locations/popular :", e)
        return jsonify({"error": "Erreur serveur"}), 500

# Ajouter/retirer une offre des favoris
@offres_bp.route('/offres/<int:offre_id>/favoris', methods=['POST', 'OPTIONS'])
@require_auth()
def toggle_favori(offre_id):
    """Ajouter ou retirer une offre des favoris"""
    
    # Vérifier que l'offre existe
    offre = Offre.query.get_or_404(offre_id)
    
    # Vérifier si l'offre est déjà en favori
    favori_existant = FavoriOffre.query.filter_by(
        utilisateur_id=g.user.id,
        offre_id=offre_id
    ).first()
    
    if favori_existant:
        # Retirer des favoris
        db.session.delete(favori_existant)
        db.session.commit()
        return jsonify({
            'message': 'Offre retirée des favoris',
            'is_favori': False
        })
    else:
        # Ajouter aux favoris
        nouveau_favori = FavoriOffre(
            utilisateur_id=g.user.id,
            offre_id=offre_id,
            date_ajout=datetime.utcnow()
        )
        db.session.add(nouveau_favori)
        db.session.commit()
        return jsonify({
            'message': 'Offre ajoutée aux favoris',
            'is_favori': True
        })

# Vérifier si une offre est en favori
@offres_bp.route('/offres/<int:offre_id>/favoris/status', methods=['GET', 'OPTIONS'])
@optional_auth
def check_favori_status(offre_id):
    """Vérifier si une offre est dans les favoris de l'utilisateur"""
    
    if not g.user:
        return jsonify({'is_favori': False})
    
    favori = FavoriOffre.query.filter_by(
        utilisateur_id=g.user.id,
        offre_id=offre_id
    ).first()
    
    return jsonify({'is_favori': bool(favori)})

# Récupérer les favoris d'un utilisateur
@offres_bp.route('/offres/favoris', methods=['GET', 'OPTIONS'])
@require_auth()
def get_mes_favoris():
    """Récupérer toutes les offres favorites de l'utilisateur connecté"""
    
    page = request.args.get('page', 1, type=int)
    per_page = min(request.args.get('per_page', 20, type=int), 100)
    
    favoris = db.session.query(Offre).join(FavoriOffre).filter(
        FavoriOffre.utilisateur_id == g.user.id
    ).order_by(FavoriOffre.date_ajout.desc()).paginate(
        page=page, per_page=per_page, error_out=False
    )
    
    return jsonify({
        'offres': [offre.to_dict() for offre in favoris.items],
        'total': favoris.total,
        'pages': favoris.pages,
        'current_page': page
    })

# Ajouter un commentaire à une offre
@offres_bp.route('/offres/<int:offre_id>/commentaires', methods=['POST'])
@require_auth()
def add_commentaire(offre_id):
    """Ajouter un commentaire à une offre"""
    
    # Vérifier que l'offre existe
    offre = Offre.query.get_or_404(offre_id)
    
    data = request.get_json()
    commentaire_text = data.get('commentaire', '').strip()
    parent_id = data.get('parent_id')
    
    if not commentaire_text:
        return jsonify({'error': 'Le commentaire ne peut pas être vide'}), 400
    
    # Si c'est une réponse, vérifier que le commentaire parent existe
    if parent_id:
        parent_comment = CommentaireOffre.query.get_or_404(parent_id)
        if parent_comment.offre_id != offre_id:
            return jsonify({'error': 'Commentaire parent invalide'}), 400
    
    # Créer le nouveau commentaire
    nouveau_commentaire = CommentaireOffre(
        commentaire=commentaire_text,
        utilisateur_id=g.user.id,
        offre_id=offre_id,
        parent_id=parent_id,
        date_creation=datetime.utcnow()
    )
    
    db.session.add(nouveau_commentaire)
    db.session.commit()
    
    return jsonify({
        'message': 'Commentaire ajouté avec succès',
        'commentaire': {
            'id': nouveau_commentaire.id,
            'commentaire': nouveau_commentaire.commentaire,
            'date_creation': nouveau_commentaire.date_creation.isoformat(),
            'utilisateur': {
                'id': g.user.id,
                'nom': g.user.nom,
                'prenom': g.user.prenom,
                'email': g.user.email
            },
            'parent_id': nouveau_commentaire.parent_id,
            'reponses': []
        }
    }), 201

# Récupérer les commentaires d'une offre
@offres_bp.route('/offres/<int:offre_id>/commentaires', methods=['GET'])
def get_commentaires(offre_id):
    """Récupérer tous les commentaires d'une offre"""
    
    # Vérifier que l'offre existe
    offre = Offre.query.get_or_404(offre_id)
    
    # Récupérer tous les commentaires de l'offre
    commentaires = CommentaireOffre.query.filter_by(
        offre_id=offre_id,
        parent_id=None
    ).order_by(CommentaireOffre.date_creation.desc()).all()
    
    def format_commentaire(commentaire):
        reponses = CommentaireOffre.query.filter_by(
            parent_id=commentaire.id
        ).order_by(CommentaireOffre.date_creation.asc()).all()
        
        return {
            'id': commentaire.id,
            'commentaire': commentaire.commentaire,
            'date_creation': commentaire.date_creation.isoformat(),
            'utilisateur': {
                'id': commentaire.utilisateur.id,
                'nom': commentaire.utilisateur.nom,
                'prenom': commentaire.utilisateur.prenom,
                'email': commentaire.utilisateur.email
            },
            'parent_id': commentaire.parent_id,
            'reponses': [format_commentaire(reponse) for reponse in reponses]
        }
    
    return jsonify({
        'commentaires': [format_commentaire(c) for c in commentaires],
        'total': len(commentaires)
    })

# Supprimer un commentaire
@offres_bp.route('/offres/commentaires/<int:commentaire_id>', methods=['DELETE'])
@require_auth()
def delete_commentaire(commentaire_id):
    """Supprimer un commentaire (seulement par son auteur)"""
    
    commentaire = CommentaireOffre.query.get_or_404(commentaire_id)
    
    # Vérifier que l'utilisateur est l'auteur du commentaire
    if commentaire.utilisateur_id != g.user.id:
        return jsonify({'error': 'Vous ne pouvez supprimer que vos propres commentaires'}), 403
    
    # Supprimer aussi les réponses à ce commentaire
    reponses = CommentaireOffre.query.filter_by(parent_id=commentaire_id).all()
    for reponse in reponses:
        db.session.delete(reponse)
    
    db.session.delete(commentaire)
    db.session.commit()
    
    return jsonify({'message': 'Commentaire supprimé avec succès'})

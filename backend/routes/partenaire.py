from flask import Blueprint, jsonify, request
from backend.models import CategorieOffre,  Partenaire, Offre, Abonnement, Secteur
from backend.extensions import db
from urllib.parse import unquote

partenaire_bp = Blueprint('partenaire', __name__)
import re
def slugify(text):
    return re.sub(r'\s+', '-', text.strip().lower())

def unslugify(slug):
    return slug.replace('-', ' ').title()

# Nouveau endpoint pour recherche géolocalisée des partenaires
@partenaire_bp.route('/partenaires', methods=['GET'])
def search_partenaires():
    try:
        # Base query avec abonnement actif obligatoire
        q = (
            db.session.query(Partenaire)
            .join(Abonnement)
            .filter(Abonnement.actif == True)
        )

        # Filtres géolocalisés
        ville = request.args.get("ville")
        if ville:
            ville = unquote(ville)
            q = q.filter(Partenaire.ville.ilike(f"%{ville}%"))

        commune = request.args.get("commune")
        if commune:
            commune = unquote(commune)
            q = q.filter(Partenaire.commune.ilike(f"%{commune}%"))

        # Filtre par secteur
        secteur_slug = request.args.get("secteur_slug")
        if secteur_slug:
            secteur_slug = unquote(secteur_slug)
            q = q.join(Secteur).filter(Secteur.slug == secteur_slug)

        # Tri
        sort_by = request.args.get("sort", "rating")
        if sort_by == "name":
            q = q.order_by(Partenaire.nom.asc())
        elif sort_by == "recent":
            q = q.order_by(Partenaire.date_inscription.desc())
        else:  # rating par défaut
            q = q.order_by(Partenaire.note_moyenne.desc().nullslast())

        # Pagination
        page = request.args.get("page", 1, type=int)
        per_page = request.args.get("per_page", 20, type=int)
        
        partenaires = q.limit(per_page).offset((page - 1) * per_page).all()
        total = q.count()

        result = []
        for partenaire in partenaires:
            abonnement = partenaire.abonnement
            secteur_nom = partenaire.secteur.nom if partenaire.secteur else None
            categorie_nom = partenaire.categorie_partenaire.nom if partenaire.categorie_partenaire else None

            result.append({
                'id': partenaire.id,
                'nom': partenaire.nom,
                'logo': partenaire.logo,
                'ville': partenaire.ville,
                'commune': partenaire.commune,
                'localisation': partenaire.localisation,
                'description': partenaire.description,
                'secteur': secteur_nom,
                'categorie': categorie_nom,
                'note_moyenne': partenaire.note_moyenne,
                'url': partenaire.url,
                'statut': abonnement.type_abonnement.lower() if abonnement else None,
                'offres_count': len(partenaire.offres)
            })

        return jsonify({
            "partenaires": result,
            "pagination": {
                "page": page,
                "per_page": per_page,
                "total": total,
                "pages": (total + per_page - 1) // per_page
            }
        })

    except Exception as e:
        print("🔥 Erreur backend :", e)
        return jsonify({'error': str(e)}), 500

@partenaire_bp.route('/partenaires-actifs', methods=['GET'])
def partenaires_actifs():
    try:
        partenaires = (
            db.session.query(Partenaire)
            .join(Abonnement)
            .filter(Abonnement.actif == True)
            .all()
        )
    except Exception as e:
        print("🔥 Erreur backend :", e)
        return jsonify({'error': str(e)}), 500

    result = []
    for partenaire in partenaires:
        abonnement = partenaire.abonnement
        secteur_nom = partenaire.secteur.nom if partenaire.secteur else None
        categorie_nom = partenaire.categorie_partenaire.nom if partenaire.categorie_partenaire else None

        result.append({
            'id': partenaire.id,
            'nom': partenaire.nom,
            'logo': partenaire.logo,
            'commune': partenaire.commune,
            'description': partenaire.description,
            'secteur': secteur_nom,
            'categorie': categorie_nom,
            'note_moyenne': partenaire.note_moyenne,
            'statut': abonnement.type_abonnement.lower() if abonnement else None,
        })

    return jsonify(result)

@partenaire_bp.route('/partenaires/<slug>')
def get_partenaire_by_slug(slug):
    partenaire = Partenaire.query.filter_by(url=slug).first_or_404()

    return {
        "id": partenaire.id,
        "nom": partenaire.nom,
        "secteur": partenaire.secteur.nom if partenaire.secteur else None,
        "categorie": partenaire.categorie_partenaire.nom if partenaire.categorie_partenaire else None,
        "localisation": partenaire.localisation,
        "ville": partenaire.ville,
        "commune": partenaire.commune,
        "description": partenaire.description,
        "contact": partenaire.contact,
        "date_inscription": partenaire.date_inscription.isoformat(),
        "logo": partenaire.logo,
        "url": partenaire.url,
        "reseaux": partenaire.reseaux,
        "note_moyenne": partenaire.note_moyenne,
        "photos": partenaire.photos,
        "statut": "premium" if partenaire.abonnement else "standard",
       "offres": [
    {
        "id": o.id,
        "titre": o.titre,
        "prix": o.prix,
        "image_banniere": o.image_banniere,
        "partenaire": {
            "id": partenaire.id,
            "nom": partenaire.nom,
            "logo": partenaire.logo,
            "secteur": partenaire.secteur.slug if partenaire.secteur else None
        }
    } for o in partenaire.offres
],

        "avis": [
            {
                "id": avis.id,
                "auteur": avis.utilisateur.nom if avis.utilisateur else "Anonyme",
                "commentaire": avis.commentaire,
                "note": avis.note,
                "date": avis.date.isoformat()
            } for avis in partenaire.avis
        ]
    }

    partenaire = Partenaire.query.get_or_404(id)

    return {
        "id": partenaire.id,
        "nom": partenaire.nom,
        "secteur": partenaire.secteur.nom if partenaire.secteur else None,
        "categorie": partenaire.categorie_partenaire.nom if partenaire.categorie_partenaire else None,
        "localisation": partenaire.localisation,
        "ville": partenaire.ville,
        "commune": partenaire.commune,
        "description": partenaire.description,
        "contact": partenaire.contact,
        "date_inscription": partenaire.date_inscription.isoformat(),
        "logo": partenaire.logo,
        "url": partenaire.url,
        "reseaux": partenaire.reseaux,  # JSON: { "facebook": "...", "instagram": "...", etc. }
        "note_moyenne": partenaire.note_moyenne,
        "photos": partenaire.photos,  # JSON: [url1, url2, ...]
        "offres": [
            {
                "id": offre.id,
                "titre": offre.titre,
                "prix": offre.prix,
                "image_banniere": offre.image_banniere
            } for offre in partenaire.offres
        ],
        "avis": [
            {
                "id": avis.id,
                "auteur": avis.auteur,
                "commentaire": avis.commentaire,
                "note": avis.note,
                "date": avis.date.isoformat()
            } for avis in partenaire.avis
        ],
        "abonnement": {
            "type": partenaire.abonnement.type if partenaire.abonnement else None,
            "date_debut": partenaire.abonnement.date_debut.isoformat() if partenaire.abonnement else None,
            "date_fin": partenaire.abonnement.date_fin.isoformat() if partenaire.abonnement else None
        }
    }

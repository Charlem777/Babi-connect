from flask import Blueprint, jsonify
from backend.models import CategorieOffre,  Partenaire, Offre, Abonnement, Secteur
from backend.extensions import db

partenaire_bp = Blueprint('partenaire', __name__)
import re
def slugify(text):
    return re.sub(r'\s+', '-', text.strip().lower())

def unslugify(slug):
    return slug.replace('-', ' ').title()

@partenaire_bp.route('/api/partenaires-actifs', methods=['GET'])
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

@partenaire_bp.route('/api/partenaires/<slug>', methods=['GET'])
def get_partenaire(slug):
    partenaire = Partenaire.query.filter_by(url=slug).first_or_404()

    offres = []
    for offre in partenaire.offres:
        offres.append({
            "id": offre.id,
            "titre": offre.titre,
            "description": offre.description,
            "prix": offre.prix,
            "type": offre.type_offre,
            "image": offre.image_banniere,
            "expire_le": offre.expire_le,
            "condition": offre.condition,
            "tags": offre.tags,
            "vues": offre.vues,
            "clics": offre.clics,
            "favoris": offre.favoris_count,
            "popularite": offre.popularite,
            "options": [
                {
                    "nom": opt.nom,
                    "description": opt.description,
                    "prix": opt.prix,
                    "duree": opt.duree
                } for opt in offre.options
            ],
            "photos": [photo.url for photo in offre.photos],
            "commentaires": [
                {
                    "nom": p.utilisateur.nom,
                    "photo": p.utilisateur.photo_profil,
                    "commentaire": p.commentaire,
                    "date": p.date_participation
                }
                for p in offre.participations if p.commentaire
            ]
        })

    avis = [
        {
            "note": a.note,
            "commentaire": a.commentaire,
            "date": a.date_avis.isoformat(),
            "utilisateur": {
                "nom": a.utilisateur.nom,
                "photo": a.utilisateur.photo_profil
            }
        } for a in partenaire.avis
    ]

    return jsonify({
        "id": partenaire.id,
        "nom": partenaire.nom,
        "secteur": partenaire.secteur,
        "description": partenaire.description,
        "ville": partenaire.ville,
        "commune": partenaire.commune,
        "localisation": partenaire.localisation,
        "contact": partenaire.contact,
        "date_inscription": partenaire.date_inscription,
        "note_moyenne": partenaire.note_moyenne,
        "logo": partenaire.logo,
        "url": partenaire.url,
        "statut": "premium" if any(ab.actif for ab in partenaire.abonnements) else "standard",
        "reseaux": partenaire.reseaux or {},
        "photos": partenaire.photos or [],
        "categorie": partenaire.categorie_partenaire.nom if partenaire.categorie_partenaire else None,
        "offres": offres,
        "avis": avis
    })



from datetime import datetime
from sqlalchemy import UniqueConstraint
from backend.extensions import db
from werkzeug.security import check_password_hash
from werkzeug.security import generate_password_hash

# ============================
# 🏷️ Secteur
# ============================
class Secteur(db.Model):
    __tablename__ = 'secteur'
    __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(100), unique=True, nullable=False)
    slug = db.Column(db.String(120), unique=True, index=True)
    description = db.Column(db.Text)
    photo = db.Column(db.String(250))  # URL ou chemin vers l'image

    partenaires = db.relationship('Partenaire', back_populates='secteur', lazy=True)
    categories_partenaire = db.relationship('CategoriePartenaire', back_populates='secteur', lazy=True)
    def to_dict(self):
            return {
                "id": self.id,
                "nom": self.nom,
                "slug": self.slug,
                "description": self.description,
                "photo": self.photo
            }
# ============================
# 🔧 Catégorie de Partenaire
# ============================
class CategoriePartenaire(db.Model):
    __tablename__ = 'categorie_partenaire'
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(100), nullable=False, unique=True)
    slug = db.Column(db.String(120), unique=True, index=True)
    description = db.Column(db.Text)

    secteur_id = db.Column(db.Integer, db.ForeignKey("secteur.id"), nullable=False)
    secteur = db.relationship("Secteur", back_populates="categories_partenaire", lazy=True)

    partenaires = db.relationship("Partenaire", back_populates="categorie_partenaire", lazy=True)
    def to_dict(self):
        return {
            "id": self.id,
            "nom": self.nom,
            "slug": self.slug,
            "description": self.description,
            "secteur_id": self.secteur_id,
            "secteur_nom": self.secteur.nom if self.secteur else None
        }



# ============================
# 🧑‍💼 Partenaire
# ============================
class Partenaire(db.Model):
    __tablename__ = 'partenaire'
    __table_args__ = (
    db.UniqueConstraint('email', name='uq_partenaire_email'),
)
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(100), nullable=False)

    secteur_id = db.Column(db.Integer, db.ForeignKey('secteur.id', name='fk_partenaire_secteur'), nullable=False)
    secteur = db.relationship('Secteur', back_populates='partenaires', lazy=True)
    mot_de_passe = db.Column(db.String(255), nullable=True)  # ← temporairement
    email = db.Column(db.String(120), nullable=True, unique=True)  # ← temporairement

    categorie_partenaire_id = db.Column(db.Integer, db.ForeignKey("categorie_partenaire.id", name="fk_partenaire_categorie"), nullable=False)
    categorie_partenaire = db.relationship("CategoriePartenaire", back_populates="partenaires", lazy=True)

    localisation = db.Column(db.String(150))
    ville = db.Column(db.String(100))
    commune = db.Column(db.String(100))
    description = db.Column(db.Text)
    contact = db.Column(db.String(100))
    date_inscription = db.Column(db.DateTime, default=datetime.utcnow)
    logo = db.Column(db.String(250))
    url = db.Column(db.String(250))
    reseaux = db.Column(db.JSON)
    note_moyenne = db.Column(db.Float, default=0)
    photos = db.Column(db.JSON)

    offres = db.relationship("Offre", back_populates="partenaire", lazy=True)
    abonnement = db.relationship("Abonnement", back_populates="partenaire", uselist=False)
    avis = db.relationship('AvisPartenaire', back_populates='partenaire', lazy=True)
    def to_dict(self):
        return {
            "id": self.id,
            "nom": self.nom,
            "ville": self.ville,
            "commune": self.commune,
            "localisation": self.localisation,
            "description": self.description,
            "logo": self.logo,
            "url": self.url,
            "note_moyenne": self.note_moyenne,
            "secteur": {
                "id": self.secteur.id,
                "nom": self.secteur.nom
            } if self.secteur else None,
            "categorie": {
                "id": self.categorie_partenaire.id,
                "nom": self.categorie_partenaire.nom
            } if self.categorie_partenaire else None,
            "date_inscription": self.date_inscription.isoformat(),
            "abonnement": {
            "id": self.abonnement.id if self.abonnement else None,  # ← AJOUT ESSENTIEL
            "type": self.abonnement.type if self.abonnement else None,
            "actif": self.abonnement.actif if self.abonnement else False,
            "expire_le": self.abonnement.date_fin.isoformat() if self.abonnement and self.abonnement.date_fin else None
        }

        }

# ============================
# 👤 Utilisateur
# ============================
class Utilisateur(db.Model):
    __tablename__ = 'utilisateur'
    id = db.Column(db.Integer, primary_key=True)
    photo_profil = db.Column(db.String(250))
    type_utilisateur = db.Column(db.String(50))  # Client / Partenaire / Admin
    nom = db.Column(db.String(100), nullable=False)
    prenom = db.Column(db.String(100))
    genre = db.Column(db.String(10)) 
    date_naissance = db.Column(db.Date)
    email = db.Column(db.String(120), unique=True, nullable=False)
    budget = db.Column(db.Float)
    ville = db.Column(db.String(100))
    commune = db.Column(db.String(100))
    telephone = db.Column(db.String(20))
    mot_de_passe = db.Column(db.String(255), nullable=False)  # ← ajoute cette ligne
    favoris = db.relationship("FavoriOffre", back_populates="utilisateur", lazy=True)

# ============================
# 💼 Abonnement
# ============================
class Abonnement(db.Model):
    __tablename__ = 'abonnement'
    id = db.Column(db.Integer, primary_key=True)

    partenaire_id = db.Column(db.Integer, db.ForeignKey('partenaire.id', name='fk_abonnement_partenaire'), nullable=False)
    partenaire = db.relationship('Partenaire', back_populates='abonnement', lazy=True)

    type = db.Column(db.Enum('basique', 'premium', name='type_abonnement'), nullable=False)
    date_debut = db.Column(db.DateTime, default=datetime.utcnow)
    date_fin = db.Column(db.DateTime)
    actif = db.Column(db.Boolean, default=True)
    offre_tag_association = db.Table('offre_tag_association',
    db.Column('offre_id', db.Integer, db.ForeignKey('offre.id'), primary_key=True),
    db.Column('tag_id', db.Integer, db.ForeignKey('tag.id'), primary_key=True)
)
    

# ============================
# 🎯 Offre
# ============================
class Offre(db.Model):
    __tablename__ = 'offre'
    id = db.Column(db.Integer, primary_key=True)
    titre = db.Column(db.String(150), nullable=False)
    description = db.Column(db.Text)
    prix = db.Column(db.Float)
    type_offre = db.Column(db.String(50))
    ville = db.Column(db.String(100))
    commune = db.Column(db.String(100))
    image_banniere = db.Column(db.String(250))
    condition = db.Column(db.Text)
    lien_externe = db.Column(db.String(250))
    expire_le = db.Column(db.DateTime)
    ambiance = db.Column(db.String(100))
    localisation = db.Column(db.String(150))
    date_publication = db.Column(db.DateTime, default=datetime.utcnow)
    photos = db.relationship("OffrePhoto", back_populates="offre", lazy=True, cascade="all, delete-orphan")

    vues = db.Column(db.Integer, default=0)
    clics = db.Column(db.Integer, default=0)
    popularite = db.Column(db.Integer, default=0)

    categorie_offre_id = db.Column(db.Integer, db.ForeignKey("categorie_offre.id"))
    partenaire_id = db.Column(db.Integer, db.ForeignKey("partenaire.id"), nullable=False)
    commentaires = db.relationship('CommentaireOffre', back_populates='offre', lazy=True, cascade="all, delete-orphan")

    __table_args__ = (
        UniqueConstraint('titre', 'partenaire_id', name='uq_offre_titre_partenaire'),
    )
    partenaire = db.relationship("Partenaire", back_populates="offres", lazy=True)
    favoris = db.relationship("FavoriOffre", back_populates="offre", lazy=True, cascade="all, delete-orphan")
    options = db.relationship('OffreOption', back_populates='parent_offre', lazy=True, cascade="all, delete-orphan")
    offre_tags = db.relationship("OffreTag", back_populates="offre", cascade="all, delete-orphan")
    
    @property
    def favoris_count(self):
        """Compte dynamique des favoris"""
        return len(self.favoris)
    
    def to_dict(self):
        partenaire_data = None
        if self.partenaire:
            partenaire_data = {
                "id": self.partenaire.id,
                "nom": self.partenaire.nom,
                "commune": self.partenaire.commune,
                "logo": self.partenaire.logo,
                "secteur": self.partenaire.secteur.slug if self.partenaire.secteur else None
            }

            return {
        "id": self.id,
        "titre": self.titre,
        "description": self.description,
        "prix": self.prix,
        "ville": self.ville,
        "commune": self.commune,
        "localisation": self.localisation,
        "image_banniere": self.image_banniere,
        "categorie_offre_id": self.categorie_offre_id,
        "secteur": self.partenaire.secteur.nom if self.partenaire and self.partenaire.secteur else None,
        "photos": [p.url for p in self.photos],
        "options": [{"id": opt.id, "nom": opt.nom, "valeur": opt.valeur, "prix_supplementaire": opt.prix_supplementaire} for opt in self.options],
        "tags": [{"id": tag.tag.id, "nom": tag.tag.nom} for tag in self.offre_tags],
        "favoris_count": self.favoris_count,
        "vues": self.vues,
        "popularite": self.popularite,
        "partenaire": partenaire_data,
        "expire_le": self.expire_le.isoformat() if self.expire_le else None,
        "date_publication": self.date_publication.isoformat() if self.date_publication else None
    }

class CommentaireOffre(db.Model):
    __tablename__ = 'commentaire_offre'
    id = db.Column(db.Integer, primary_key=True)
    commentaire = db.Column(db.Text, nullable=False)
    date_creation = db.Column(db.DateTime, default=datetime.utcnow)

    utilisateur_id = db.Column(db.Integer, db.ForeignKey('utilisateur.id'), nullable=False)
    utilisateur = db.relationship('Utilisateur', lazy=True)

    offre_id = db.Column(db.Integer, db.ForeignKey('offre.id'), nullable=False)
    offre = db.relationship('Offre', back_populates='commentaires', lazy=True)

    # Commentaire parent pour les réponses
    parent_id = db.Column(db.Integer, db.ForeignKey('commentaire_offre.id'), nullable=True)
    parent = db.relationship('CommentaireOffre', remote_side=[id], backref='reponses')

    def to_dict(self):
        return {
            'id': self.id,
            'commentaire': self.commentaire,
            'date_creation': self.date_creation.isoformat() if self.date_creation else None,
            'utilisateur': {
                'id': self.utilisateur.id,
                'nom': self.utilisateur.nom,
                'prenom': self.utilisateur.prenom,
                'email': self.utilisateur.email
            } if self.utilisateur else None,
            'parent_id': self.parent_id,
            'reponses': [reponse.to_dict() for reponse in self.reponses] if hasattr(self, 'reponses') else []
        }

class OffrePhoto(db.Model):
    __tablename__ = 'offre_photo'
    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String(250), nullable=False)
    date_ajout = db.Column(db.DateTime, default=datetime.utcnow)

    offre_id = db.Column(db.Integer, db.ForeignKey('offre.id'), nullable=False)
    offre = db.relationship('Offre', back_populates='photos')

class OffreOption(db.Model):
    __tablename__ = 'offre_option'
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(100), nullable=False)
    valeur = db.Column(db.String(100), nullable=True)  # ex: "Sans sucre", "XL", "Livraison express"
    prix_supplementaire = db.Column(db.Float, default=0.0)

    offre_id = db.Column(db.Integer, db.ForeignKey('offre.id'), nullable=False)
    parent_offre = db.relationship('Offre', back_populates='options')

# ============================
# 📁 Catégorie d’Offres
# ============================
class CategorieOffre(db.Model):
    __tablename__ = 'categorie_offre'
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(100), nullable=False, unique=True)
    slug = db.Column(db.String(120), unique=True, index=True)
    description = db.Column(db.Text)

    offres = db.relationship("Offre", backref="categorie_offre", lazy=True)
    def to_dict(self):
        return {
            "id": self.id,
            "nom": self.nom,
            "slug": self.slug,
            "description": self.description
        }

class FavoriOffre(db.Model):
    __tablename__ = 'favori_offre'
    id = db.Column(db.Integer, primary_key=True)
    
    utilisateur_id = db.Column(db.Integer, db.ForeignKey('utilisateur.id'), nullable=False)
    utilisateur = db.relationship('Utilisateur', back_populates="favoris", lazy=True)
    
    offre_id = db.Column(db.Integer, db.ForeignKey('offre.id'), nullable=False)
    offre = db.relationship('Offre', back_populates="favoris", lazy=True)
    
    date_ajout = db.Column(db.DateTime, default=datetime.utcnow)
    
    __table_args__ = (
        UniqueConstraint('utilisateur_id', 'offre_id', name='uq_favori_utilisateur_offre'),
    )

# ============================
# ⭐️ Avis Partenaire
# ============================
class AvisPartenaire(db.Model):
    __tablename__ = 'avis_partenaire'
    id = db.Column(db.Integer, primary_key=True)

    utilisateur_id = db.Column(db.Integer, db.ForeignKey('utilisateur.id', name='fk_avis_utilisateur'), nullable=False)
    utilisateur = db.relationship('Utilisateur', backref='avis_partenaire', lazy=True)

    partenaire_id = db.Column(db.Integer, db.ForeignKey('partenaire.id', name='fk_avis_partenaire'), nullable=False)
    partenaire = db.relationship('Partenaire', back_populates='avis', lazy=True)

    note = db.Column(db.Integer, nullable=False)
    commentaire = db.Column(db.Text)
    date = db.Column(db.DateTime, default=datetime.utcnow)
    visible = db.Column(db.Boolean, default=True)

# ============================
# 🏷️ Tags
# ============================
class Tag(db.Model):
    __tablename__ = "tag"
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(50), unique=True, nullable=False)

    offre_tags = db.relationship("OffreTag", back_populates="tag")


class OffreTag(db.Model):
    __tablename__ = "offre_tag"
    id = db.Column(db.Integer, primary_key=True)
    offre_id = db.Column(db.Integer, db.ForeignKey("offre.id"), nullable=False)
    tag_id = db.Column(db.Integer, db.ForeignKey("tag.id"), nullable=False)

    offre = db.relationship("Offre", back_populates="offre_tags")  # ✅ Garder une seule fois
    tag = db.relationship("Tag", back_populates="offre_tags")      # ✅ Manquait dans ton code

# ============================
# 💬 Conversation
# ============================
class Conversation(db.Model):
    __tablename__ = 'conversation'
    
    id = db.Column(db.String(36), primary_key=True)  # UUID
    client_id = db.Column(db.Integer, db.ForeignKey('utilisateur.id'), nullable=True)  # Peut être null pour invités
    partenaire_id = db.Column(db.Integer, db.ForeignKey('partenaire.id'), nullable=False)
    guest_name = db.Column(db.String(100), nullable=True)  # Nom de l'invité si pas connecté
    guest_email = db.Column(db.String(120), nullable=True)  # Email de l'invité si pas connecté
    sujet = db.Column(db.String(200), nullable=True)
    statut = db.Column(db.String(20), default='active')  # active, archived, closed
    date_creation = db.Column(db.DateTime, default=datetime.utcnow)
    derniere_activite = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relations
    client = db.relationship('Utilisateur', backref='conversations_client', lazy=True)
    partenaire = db.relationship('Partenaire', backref='conversations_partenaire', lazy=True)
    messages = db.relationship('Message', backref='conversation', lazy=True, cascade='all, delete-orphan')
    
    def to_dict(self):
        return {
            'id': self.id,
            'client_id': self.client_id,
            'partenaire_id': self.partenaire_id,
            'guest_name': self.guest_name,
            'guest_email': self.guest_email,
            'sujet': self.sujet,
            'statut': self.statut,
            'date_creation': self.date_creation.isoformat() if self.date_creation else None,
            'derniere_activite': self.derniere_activite.isoformat() if self.derniere_activite else None,
            'partenaire': {
                'id': self.partenaire.id,
                'nom': self.partenaire.nom,
                'logo': self.partenaire.logo
            } if self.partenaire else None,
            'client': {
                'id': self.client.id,
                'nom': self.client.nom,
                'prenom': self.client.prenom
            } if self.client else None,
            'dernier_message': self.messages[-1].to_dict() if self.messages else None,
            'messages_count': len(self.messages)
        }

# ============================
# 💬 Message
# ============================
class Message(db.Model):
    __tablename__ = 'message'
    
    id = db.Column(db.Integer, primary_key=True)
    conversation_id = db.Column(db.String(36), db.ForeignKey('conversation.id'), nullable=False)
    expediteur_type = db.Column(db.String(20), nullable=False)  # 'client', 'partenaire', 'guest'
    expediteur_id = db.Column(db.Integer, nullable=True)  # ID du client ou partenaire
    contenu = db.Column(db.Text, nullable=False)
    type_message = db.Column(db.String(20), default='text')  # text, image, file
    fichier_url = db.Column(db.String(500), nullable=True)
    lu = db.Column(db.Boolean, default=False)
    date_envoi = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'conversation_id': self.conversation_id,
            'expediteur_type': self.expediteur_type,
            'expediteur_id': self.expediteur_id,
            'contenu': self.contenu,
            'type_message': self.type_message,
            'fichier_url': self.fichier_url,
            'lu': self.lu,
            'date_envoi': self.date_envoi.isoformat() if self.date_envoi else None
        }

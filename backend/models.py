from datetime import datetime
from sqlalchemy import UniqueConstraint
from backend.extensions import db

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

    partenaires = db.relationship('Partenaire', back_populates='secteur', lazy=True)
    categories_partenaire = db.relationship('CategoriePartenaire', back_populates='secteur', lazy=True)

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

# ============================
# 🧑‍💼 Partenaire
# ============================
class Partenaire(db.Model):
    __tablename__ = 'partenaire'
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(100), nullable=False)

    secteur_id = db.Column(db.Integer, db.ForeignKey('secteur.id', name='fk_partenaire_secteur'), nullable=False)
    secteur = db.relationship('Secteur', back_populates='partenaires', lazy=True)

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

    offres = db.relationship("Offre", backref="partenaire", lazy=True)
    abonnement = db.relationship("Abonnement", back_populates="partenaire", uselist=False)
    avis = db.relationship('AvisPartenaire', back_populates='partenaire', lazy=True)

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

    favoris = db.relationship("Favori", back_populates="utilisateur", lazy=True)

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
    favoris_count = db.Column(db.Integer, default=0)
    popularite = db.Column(db.Integer, default=0)

    categorie_offre_id = db.Column(db.Integer, db.ForeignKey("categorie_offre.id"))
    partenaire_id = db.Column(db.Integer, db.ForeignKey("partenaire.id"), nullable=False)

    __table_args__ = (
        UniqueConstraint('titre', 'partenaire_id', name='uq_offre_titre_partenaire'),
    )

    favoris = db.relationship("Favori", back_populates="offre", lazy=True)
    options = db.relationship('OffreOption', back_populates='parent_offre', lazy=True, cascade="all, delete-orphan")
    offre_tags = db.relationship("OffreTag", back_populates="offre", cascade="all, delete-orphan")
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

class Favori(db.Model):
    __tablename__ = 'favori'
    id = db.Column(db.Integer, primary_key=True)

    utilisateur_id = db.Column(
        db.Integer,
        db.ForeignKey('utilisateur.id', name='fk_favori_utilisateur'),
        nullable=False
    )
    utilisateur = db.relationship("Utilisateur", back_populates="favoris", lazy=True)


    offre_id = db.Column(
        db.Integer,
        db.ForeignKey('offre.id', name='fk_favori_offre'),
        nullable=False
    )
    offre = db.relationship("Offre", back_populates="favoris", lazy=True)


    date_ajout = db.Column(db.DateTime, default=datetime.utcnow)

    __table_args__ = (
        UniqueConstraint('utilisateur_id', 'offre_id', name='uq_utilisateur_offre_favori'),
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




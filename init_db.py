from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import declarative_base, sessionmaker, relationship
from datetime import datetime

# 📦 Configuration de la base
SQLALCHEMY_DATABASE_URL = "sqlite:///babi_connect.db"  # ou ton URL PostgreSQL/MySQL

engine = create_engine(SQLALCHEMY_DATABASE_URL, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# 👥 Modèles
class Partenaire(Base):
    __tablename__ = "partenaires"
    id = Column(Integer, primary_key=True, index=True)
    nom = Column(String(255))
    email = Column(String(255))
    telephone = Column(String(255))
    offres = relationship("Offre", back_populates="partenaire")

class Offre(Base):
    __tablename__ = "offres"
    id = Column(Integer, primary_key=True, index=True)
    titre = Column(String(255))
    description = Column(Text)
    date_publication = Column(DateTime, default=datetime.utcnow)
    partenaire_id = Column(Integer, ForeignKey("partenaires.id"))
    partenaire = relationship("Partenaire", back_populates="offres")

class Utilisateur(Base):
    __tablename__ = "utilisateurs"
    id = Column(Integer, primary_key=True, index=True)
    nom = Column(String(255))
    email = Column(String(255))
    mot_de_passe = Column(String(255))

class Abonnement(Base):
    __tablename__ = "abonnements"
    id = Column(Integer, primary_key=True, index=True)
    utilisateur_id = Column(Integer, ForeignKey("utilisateurs.id"))
    partenaire_id = Column(Integer, ForeignKey("partenaires.id"))
    date_debut = Column(DateTime, default=datetime.utcnow)
    date_fin = Column(DateTime)

    partenaire = relationship("Partenaire")

# 🧱 Création de la base
def init_db():
    Base.metadata.create_all(bind=engine)

if __name__ == "__main__":
    init_db()
    print("✅ Base de données créée avec succès !")

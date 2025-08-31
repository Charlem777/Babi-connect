# 🇨🇮 Babi Connect - Plateforme Ivoirienne de Mise en Relation

> **La plateforme qui unit les Ivoiriens** - Connectez clients et partenaires locaux à Abidjan et en Côte d'Ivoire

![Babi Connect](https://img.shields.io/badge/Status-En%20Développement-orange)
![Python](https://img.shields.io/badge/Python-3.9+-blue)
![Vue.js](https://img.shields.io/badge/Vue.js-3.0+-green)
![Flask](https://img.shields.io/badge/Flask-2.0+-red)

## 🎯 À propos

Babi Connect est une plateforme moderne de mise en relation entre clients et partenaires de services en Côte d'Ivoire. Inspirée par l'identité culturelle ivoirienne, elle facilite la découverte et la réservation de services locaux dans tous les secteurs.

### ✨ Fonctionnalités principales

- 🔍 **Recherche avancée** avec filtres géographiques et par secteur
- 💬 **Chat temps réel** entre clients et partenaires
- ⭐ **Système d'avis** et de favoris
- 🏪 **Profils partenaires** détaillés avec galeries
- 📱 **Design responsive** mobile-first
- 🎨 **Identité ivoirienne** authentique (couleurs nationales, éléphant symbolique)

## 🏗️ Architecture Technique

### Backend (Flask)
- **Framework**: Flask + SQLAlchemy
- **Base de données**: PostgreSQL/SQLite
- **Authentification**: JWT avec rôles (client, partenaire, admin, invité)
- **API REST** complète avec 50+ endpoints
- **Migrations**: Alembic pour la gestion de schéma

### Frontend (Vue.js)
- **Framework**: Vue 3 + Composition API
- **State Management**: Pinia stores
- **Styling**: Tailwind CSS avec thème ivoirien
- **Build**: Vite
- **Composants**: 69 composants modulaires

## 🚀 Installation et Démarrage

### Prérequis
- Python 3.9+
- Node.js 16+
- npm ou yarn

### 1. Cloner le projet
```bash
git clone https://github.com/votre-username/babi-connect.git
cd babi-connect
```

### 2. Configuration Backend
```bash
# Créer l'environnement virtuel
python -m venv venv
source venv/bin/activate  # Sur Windows: venv\Scripts\activate

# Installer les dépendances
pip install -r requirements.txt

# Configurer la base de données
flask db upgrade

# Lancer le serveur Flask
flask run
```

### 3. Configuration Frontend
```bash
cd frontend/vue-project

# Installer les dépendances
npm install

# Lancer le serveur de développement
npm run dev
```

### 4. Accès à l'application
- **Frontend**: http://localhost:5173
- **Backend API**: http://localhost:5000
- **Admin**: http://localhost:5173/admin

## 📁 Structure du Projet

```
babi-connect/
├── backend/                 # API Flask
│   ├── models.py           # Modèles SQLAlchemy
│   ├── routes/             # Routes API organisées
│   ├── middlewares/        # Authentification & sécurité
│   └── static/uploads/     # Fichiers uploadés
├── frontend/vue-project/   # Application Vue.js
│   ├── src/components/     # 69 composants Vue
│   ├── src/views/          # Pages principales
│   ├── src/stores/         # Stores Pinia
│   └── src/assets/         # Assets statiques
├── migrations/             # Migrations de base de données
└── instance/              # Configuration locale
```

## 🎨 Identité Visuelle

### Couleurs Nationales
- **Orange**: `#FF8C00` - Couleur principale
- **Vert**: `#228B22` - Couleur secondaire  
- **Jaune**: `#FFD700` - Accents

### Éléments Culturels
- 🐘 **Éléphant symbolique** - Logo et mascotte
- 🇨🇮 **Drapeau ivoirien** - Intégration subtile
- 🎨 **Motifs Kente** - Patterns géométriques traditionnels

## 🔧 API Endpoints Principaux

### Authentification
- `POST /api/login` - Connexion utilisateur
- `POST /api/register` - Inscription
- `POST /api/guest-session` - Session invité

### Offres
- `GET /api/offres` - Liste des offres avec filtres
- `GET /api/offres/{id}` - Détail d'une offre
- `POST /api/offres/{id}/favoris` - Ajouter aux favoris

### Chat
- `GET /api/chat/conversations` - Conversations utilisateur
- `POST /api/chat/conversations` - Créer une conversation
- `POST /api/chat/conversations/{id}/messages` - Envoyer un message

## 🛠️ Technologies Utilisées

### Backend
- **Flask** - Framework web Python
- **SQLAlchemy** - ORM pour base de données
- **Flask-Migrate** - Gestion des migrations
- **Flask-JWT-Extended** - Authentification JWT
- **Flask-CORS** - Gestion CORS

### Frontend
- **Vue 3** - Framework JavaScript progressif
- **Pinia** - State management moderne
- **Vue Router** - Routage SPA
- **Tailwind CSS** - Framework CSS utility-first
- **Vite** - Build tool rapide

## 🚦 Statut du Développement

### ✅ Fonctionnalités Complètes
- Authentification multi-rôles
- Système d'offres avec CRUD complet
- Chat temps réel client-partenaire
- Filtres géographiques avancés
- Interface responsive moderne
- Système de commentaires et favoris

### 🔄 En Cours
- Système de paiement intégré
- Notifications push
- Analytics avancées
- API mobile

### 📋 Roadmap
- Application mobile React Native
- Intégration Orange Money/MTN Mobile Money
- Système de réservation en ligne
- Marketplace e-commerce

## 🤝 Contribution

1. Fork le projet
2. Créer une branche feature (`git checkout -b feature/nouvelle-fonctionnalite`)
3. Commit les changements (`git commit -m 'Ajout nouvelle fonctionnalité'`)
4. Push vers la branche (`git push origin feature/nouvelle-fonctionnalite`)
5. Ouvrir une Pull Request

## 📄 Licence

Ce projet est sous licence MIT. Voir le fichier `LICENSE` pour plus de détails.

## 👥 Équipe

- **Développeur Principal**: Votre nom
- **Design UI/UX**: Équipe design
- **Product Owner**: Équipe produit

## 📞 Contact

- **Email**: contact@babiconnect.ci
- **Site Web**: https://babiconnect.ci
- **LinkedIn**: [Babi Connect](https://linkedin.com/company/babiconnect)

---

**Fait avec ❤️ en Côte d'Ivoire** 🇨🇮

import jwt
from flask import request, jsonify, g
from functools import wraps
from backend.models import Partenaire, Utilisateur
from backend.config import SECRET_KEY

# 🔍 Décodage du token JWT
def decode_jwt_token(token):
    try:
        # Vérifier que le token n'est pas vide
        if not token:
            print("❌ Token vide")
            return None
            
        # Vérifier le format JWT basique (3 parties séparées par des points)
        parts = token.split('.')
        if len(parts) != 3:
            print(f"❌ Token invalide: format incorrect - {len(parts)} parties au lieu de 3")
            return None
            
        # Vérifier que chaque partie n'est pas vide
        if not all(parts):
            print("❌ Token invalide: parties vides détectées")
            return None
            
        print(f"✅ Token format valide: {len(token)} caractères")
        return jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
    except jwt.ExpiredSignatureError:
        print("⏰ Token expiré")
        return None
    except jwt.InvalidTokenError as e:
        print(f"❌ Token invalide: {str(e)}")
        return None

# 🔐 Middleware optionnel (permet invités)
def optional_auth(f):
    """Middleware qui permet l'accès aux invités mais injecte l'utilisateur si connecté"""
    @wraps(f)
    def wrapper(*args, **kwargs):
        if request.method == 'OPTIONS':
            return '', 200

        token = request.headers.get("Authorization", "").replace("Bearer ", "")
        
        if not token:
            # Pas de token = invité
            g.user = None
            g.role = 'guest'
            g.is_authenticated = False
            return f(*args, **kwargs)

        payload = decode_jwt_token(token)
        if not payload:
            # Token invalide = invité
            g.user = None
            g.role = 'guest'
            g.is_authenticated = False
            return f(*args, **kwargs)

        # Token valide
        role_in_token = payload.get("role", "").lower()
        
        if role_in_token == 'guest':
            g.user = {
                'id': payload.get('guest_id'),
                'name': payload.get('name'),
                'email': payload.get('email')
            }
            g.role = 'guest'
            g.is_authenticated = False
        else:
            user_id = payload.get("id")
            
            if role_in_token == "partenaire":
                user = Partenaire.query.filter_by(id=user_id).first()
            elif role_in_token in ["admin", "client"]:
                user = Utilisateur.query.filter_by(id=user_id, type_utilisateur=role_in_token.capitalize()).first()
            else:
                g.user = None
                g.role = 'guest'
                g.is_authenticated = False
                return f(*args, **kwargs)

            if user:
                g.user = user
                g.role = role_in_token
                g.is_authenticated = True
            else:
                g.user = None
                g.role = 'guest'
                g.is_authenticated = False

        return f(*args, **kwargs)
    return wrapper

# 🔐 Middleware strict (authentification requise)
def require_auth(role=None):
    """Middleware qui exige une authentification valide"""
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            if request.method == 'OPTIONS':
                return '', 200

            auth_header = request.headers.get("Authorization", "")
            print(f"🔍 require_auth - Authorization header: '{auth_header}'")
            token = auth_header.replace("Bearer ", "")
            print(f"🔍 require_auth - Token after Bearer removal: '{token[:50] if token else 'EMPTY'}...'")
            
            payload = decode_jwt_token(token)

            if not payload:
                return jsonify({"error": "Authentification requise"}), 401

            role_in_token = payload.get("role", "").lower()
            
            # Les invités ne peuvent pas accéder aux routes protégées
            if role_in_token == 'guest':
                return jsonify({"error": "Connexion requise pour accéder à cette fonctionnalité"}), 401

            user_id = payload.get("id")

            # 🔍 Vérification du rôle
            if role and role_in_token != role.lower():
                return jsonify({"error": "Accès refusé"}), 403

            # 🔄 Injection dynamique selon le rôle
            if role_in_token == "partenaire":
                user = Partenaire.query.filter_by(id=user_id).first()
            elif role_in_token in ["admin", "client"]:
                user = Utilisateur.query.filter_by(id=user_id, type_utilisateur=role_in_token.capitalize()).first()
            else:
                return jsonify({"error": "Rôle inconnu"}), 403

            if not user:
                return jsonify({"error": "Utilisateur introuvable"}), 404

            g.user = user
            g.role = role_in_token
            g.is_authenticated = True

            return f(*args, **kwargs)
        return wrapper
    return decorator

# 🔐 Middleware pour les messages (permet invités mais avec restrictions)
def require_auth_for_messaging(f):
    """Middleware spécial pour les messages - permet aux invités de démarrer une conversation"""
    @wraps(f)
    def wrapper(*args, **kwargs):
        if request.method == 'OPTIONS':
            return '', 200

        token = request.headers.get("Authorization", "").replace("Bearer ", "")
        
        if not token:
            return jsonify({"error": "Token requis pour envoyer des messages"}), 401

        payload = decode_jwt_token(token)
        if not payload:
            return jsonify({"error": "Token invalide"}), 401

        role_in_token = payload.get("role", "").lower()
        
        if role_in_token == 'guest':
            # Les invités peuvent envoyer des messages avec des infos limitées
            g.user = {
                'id': payload.get('guest_id'),
                'name': payload.get('name'),
                'email': payload.get('email')
            }
            g.role = 'guest'
            g.is_authenticated = False
        else:
            user_id = payload.get("id")
            
            if role_in_token == "partenaire":
                user = Partenaire.query.filter_by(id=user_id).first()
            elif role_in_token in ["admin", "client"]:
                user = Utilisateur.query.filter_by(id=user_id, type_utilisateur=role_in_token.capitalize()).first()
            else:
                return jsonify({"error": "Rôle inconnu"}), 403

            if not user:
                return jsonify({"error": "Utilisateur introuvable"}), 404

            g.user = user
            g.role = role_in_token
            g.is_authenticated = True

        return f(*args, **kwargs)
    return wrapper

import datetime
import uuid
import sys
from flask import Blueprint, request, jsonify, session
import jwt
from werkzeug.security import check_password_hash, generate_password_hash
from backend.models import Utilisateur, Partenaire
from backend.utils.jwt import generate_token
from backend.config import SECRET_KEY
from backend.extensions import db

auth_bp = Blueprint('auth', __name__, url_prefix='/api')

@auth_bp.route('/login', methods=['POST'])
def login():
    if request.method != 'POST':
        return '', 405
    try:
        data = request.get_json(force=True)
    except Exception:
        return jsonify({'error': 'Format JSON invalide'}), 400

    email = data.get('email')
    password = data.get('password')
    role = data.get('role')
    print(" Tentative de connexion :", email, role)
    sys.stdout.flush()

    if not email or not password or not role:
        return jsonify({'error': 'Champs requis manquants'}), 400

    if role in ['admin', 'client']:
        user = Utilisateur.query.filter_by(email=email, type_utilisateur=role.capitalize()).first()
        if not user or not check_password_hash(user.mot_de_passe, password):
            return jsonify({'error': 'Identifiants invalides'}), 401
        token = generate_token(user.id, role)
        return jsonify({
            'token': token, 
            'role': role,
            'user': {
                'id': user.id,
                'nom': user.nom,
                'prenom': user.prenom,
                'email': user.email,
                'type_utilisateur': user.type_utilisateur
            }
        })

    elif role == 'partenaire':
        partenaire = Partenaire.query.filter_by(email=email).first()
        if not partenaire or not check_password_hash(partenaire.mot_de_passe, password):
            return jsonify({'error': 'Identifiants invalides'}), 401
        token = generate_token(partenaire.id, role)
        return jsonify({
            'token': token, 
            'role': role,
            'user': {
                'id': partenaire.id,
                'nom': partenaire.nom,
                'email': partenaire.email,
                'slug': partenaire.url,
                'photo_profil': partenaire.logo
            }
        })

    return jsonify({'error': 'Rôle invalide'}), 400

@auth_bp.route('/register', methods=['POST'])
def register():
    try:
        data = request.get_json(force=True)
    except Exception:
        return jsonify({'error': 'Format JSON invalide'}), 400

    email = data.get('email')
    password = data.get('password')
    nom = data.get('nom')
    prenom = data.get('prenom')
    role = data.get('role', 'client')

    if not all([email, password, nom, prenom]):
        return jsonify({'error': 'Champs requis manquants'}), 400

    # Vérifier si l'utilisateur existe déjà
    existing_user = Utilisateur.query.filter_by(email=email).first()
    if existing_user:
        return jsonify({'error': 'Un compte avec cet email existe déjà'}), 400

    # Créer le nouvel utilisateur
    new_user = Utilisateur(
        email=email,
        mot_de_passe=generate_password_hash(password),
        nom=nom,
        prenom=prenom,
        type_utilisateur=role.capitalize(),
        date_creation=datetime.datetime.utcnow()
    )

    try:
        db.session.add(new_user)
        db.session.commit()
        
        token = generate_token(new_user.id, role)
        return jsonify({
            'token': token,
            'role': role,
            'user': {
                'id': new_user.id,
                'nom': new_user.nom,
                'prenom': new_user.prenom,
                'email': new_user.email,
                'type_utilisateur': new_user.type_utilisateur
            },
            'message': 'Compte créé avec succès'
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Erreur lors de la création du compte'}), 500

@auth_bp.route('/guest-session', methods=['POST'])
def create_guest_session():
    """Créer une session invité temporaire"""
    try:
        data = request.get_json(force=True)
    except Exception:
        data = {}
    
    guest_id = str(uuid.uuid4())
    guest_name = data.get('name', f'Invité_{guest_id[:8]}')
    guest_email = data.get('email')
    
    # Créer un token temporaire pour l'invité
    guest_token = jwt.encode({
        'guest_id': guest_id,
        'name': guest_name,
        'email': guest_email,
        'role': 'guest',
        'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=24)
    }, SECRET_KEY, algorithm='HS256')
    
    return jsonify({
        'token': guest_token,
        'role': 'guest',
        'guest': {
            'id': guest_id,
            'name': guest_name,
            'email': guest_email
        }
    })

@auth_bp.route('/verify-token', methods=['POST'])
def verify_token():
    """Vérifier la validité d'un token"""
    print("🚨 VERIFY_TOKEN ROUTE CALLED")
    sys.stdout.flush()
    
    token = request.headers.get('Authorization', '').replace('Bearer ', '')
    
    print(f"🔐 verify_token called with token: {token[:50] if token else 'None'}...")
    print(f"🔐 Token length: {len(token) if token else 0}")
    print(f"🔐 Token type: {type(token)}")
    sys.stdout.flush()
    
    if not token:
        print("❌ Token manquant")
        sys.stdout.flush()
        return jsonify({'valid': False, 'error': 'Token manquant'}), 401
    
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
        print(f"✅ Token décodé: {payload}")
        sys.stdout.flush()
        
        # Token invité
        if payload.get('role') == 'guest':
            print("👤 Token invité validé")
            sys.stdout.flush()
            return jsonify({
                'valid': True,
                'role': 'guest',
                'guest': {
                    'id': payload.get('guest_id'),
                    'name': payload.get('name'),
                    'email': payload.get('email')
                }
            })
        
        # Token utilisateur normal
        user_id = payload.get('id')
        role = payload.get('role')
        print(f"🔍 Recherche utilisateur: id={user_id}, role={role}")
        sys.stdout.flush()
        
        if role == 'partenaire':
            user = Partenaire.query.get(user_id)
        else:
            user = Utilisateur.query.filter_by(id=user_id, type_utilisateur=role.capitalize()).first()
        
        if not user:
            print(f"❌ Utilisateur introuvable: id={user_id}, role={role}")
            sys.stdout.flush()
            return jsonify({'valid': False, 'error': 'Utilisateur introuvable'}), 404
        
        print(f"✅ Utilisateur trouvé: {user.nom}")
        sys.stdout.flush()
        return jsonify({
            'valid': True,
            'role': role,
            'user': user.to_dict() if hasattr(user, 'to_dict') else {
                'id': user.id,
                'nom': user.nom,
                'email': user.email
            }
        })
        
    except jwt.ExpiredSignatureError:
        print("❌ Token expiré")
        sys.stdout.flush()
        return jsonify({'valid': False, 'error': 'Token expiré'}), 401
    except jwt.InvalidTokenError as e:
        print(f"❌ Token invalide: {e}")
        print(f"❌ Token reçu: '{token}'")
        sys.stdout.flush()
        return jsonify({'valid': False, 'error': 'Token invalide'}), 401

@auth_bp.route('/logout', methods=['POST'])
def logout():
    """Déconnexion (côté client principalement)"""
    return jsonify({'message': 'Déconnexion réussie'})

import uuid
from datetime import datetime
from flask import Blueprint, request, jsonify, g
from backend.models import Conversation, Message, Partenaire, Utilisateur
from backend.middlewares.auth import require_auth_for_messaging, require_auth, optional_auth
from backend.extensions import db

chat_bp = Blueprint('chat', __name__, url_prefix='/api/chat')

@chat_bp.route('/conversations', methods=['GET'])
@require_auth()
def get_conversations():
    """Récupérer les conversations de l'utilisateur connecté"""
    try:
        if g.role == 'partenaire':
            conversations = Conversation.query.filter_by(partenaire_id=g.user.id).order_by(Conversation.derniere_activite.desc()).all()
        elif g.role in ['client', 'admin']:
            conversations = Conversation.query.filter_by(client_id=g.user.id).order_by(Conversation.derniere_activite.desc()).all()
        else:
            return jsonify({'error': 'Type d\'utilisateur non supporté'}), 400
        
        return jsonify({
            'conversations': [conv.to_dict() for conv in conversations]
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@chat_bp.route('/conversations/<conversation_id>', methods=['GET'])
@require_auth_for_messaging
def get_conversation(conversation_id):
    """Récupérer une conversation spécifique avec ses messages"""
    try:
        conversation = Conversation.query.get(conversation_id)
        if not conversation:
            return jsonify({'error': 'Conversation introuvable'}), 404
        
        # Vérifier les permissions
        if g.role == 'partenaire' and conversation.partenaire_id != g.user.id:
            return jsonify({'error': 'Accès refusé'}), 403
        elif g.role in ['client', 'admin'] and conversation.client_id != g.user.id:
            return jsonify({'error': 'Accès refusé'}), 403
        elif g.role == 'guest':
            # Les invités peuvent voir leurs conversations via l'ID de session
            guest_id = g.user.get('id') if isinstance(g.user, dict) else None
            if not any(msg.expediteur_type == 'guest' and str(msg.expediteur_id) == str(guest_id) 
                      for msg in conversation.messages):
                return jsonify({'error': 'Accès refusé'}), 403
        
        # Marquer les messages comme lus
        if g.role != 'guest':
            messages_non_lus = Message.query.filter_by(
                conversation_id=conversation_id,
                lu=False
            ).filter(Message.expediteur_id != g.user.id).all()
            
            for message in messages_non_lus:
                message.lu = True
            db.session.commit()
        
        messages = Message.query.filter_by(conversation_id=conversation_id).order_by(Message.date_envoi.asc()).all()
        
        return jsonify({
            'conversation': conversation.to_dict(),
            'messages': [msg.to_dict() for msg in messages]
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@chat_bp.route('/conversations', methods=['POST'])
@require_auth_for_messaging
def create_conversation():
    """Créer une nouvelle conversation"""
    try:
        print(f"🔍 create_conversation called - Role: {g.role}, User: {g.user}")
        
        data = request.get_json()
        print(f"🔍 Request data: {data}")
        
        partenaire_id = data.get('partenaire_id')
        sujet = data.get('sujet', '')
        message_initial = data.get('message')
        
        print(f"🔍 Parsed data - partenaire_id: {partenaire_id}, sujet: {sujet}, message: {message_initial}")
        
        if not partenaire_id or not message_initial:
            return jsonify({'error': 'Partenaire ID et message requis'}), 400
        
        # Vérifier que le partenaire existe
        partenaire = Partenaire.query.get(partenaire_id)
        print(f"🔍 Partenaire found: {partenaire.nom if partenaire else 'None'}")
        
        if not partenaire:
            return jsonify({'error': 'Partenaire introuvable'}), 404
        
        # Créer la conversation
        conversation_id = str(uuid.uuid4())
        print(f"🔍 Creating conversation with ID: {conversation_id}")
        
        conversation = Conversation(
            id=conversation_id,
            partenaire_id=partenaire_id,
            sujet=sujet,
            date_creation=datetime.utcnow(),
            derniere_activite=datetime.utcnow()
        )
        
        if g.role == 'guest':
            conversation.guest_name = g.user.get('name')
            conversation.guest_email = g.user.get('email')
            print(f"🔍 Guest conversation - name: {conversation.guest_name}")
        else:
            conversation.client_id = g.user.id
            print(f"🔍 Client conversation - client_id: {conversation.client_id}")
        
        db.session.add(conversation)
        print("🔍 Conversation added to session")
        
        # Créer le message initial
        message = Message(
            conversation_id=conversation_id,
            expediteur_type=g.role,
            contenu=message_initial,
            date_envoi=datetime.utcnow()
        )
        
        if g.role == 'guest':
            message.expediteur_id = None  # Les invités n'ont pas d'ID en base
        else:
            message.expediteur_id = g.user.id
        
        print(f"🔍 Message created - expediteur_type: {message.expediteur_type}, expediteur_id: {message.expediteur_id}")
        
        db.session.add(message)
        print("🔍 Message added to session")
        
        db.session.commit()
        print("🔍 Database commit successful")
        
        return jsonify({
            'conversation': conversation.to_dict(),
            'message': 'Conversation créée avec succès'
        }), 201
        
    except Exception as e:
        print(f"❌ Error in create_conversation: {str(e)}")
        print(f"❌ Error type: {type(e)}")
        import traceback
        print(f"❌ Traceback: {traceback.format_exc()}")
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@chat_bp.route('/conversations/<conversation_id>/messages', methods=['POST'])
@require_auth_for_messaging
def send_message(conversation_id):
    """Envoyer un message dans une conversation"""
    try:
        data = request.get_json()
        contenu = data.get('contenu')
        type_message = data.get('type_message', 'text')
        
        if not contenu:
            return jsonify({'error': 'Contenu du message requis'}), 400
        
        # Vérifier que la conversation existe
        conversation = Conversation.query.get(conversation_id)
        if not conversation:
            return jsonify({'error': 'Conversation introuvable'}), 404
        
        # Vérifier les permissions
        if g.role == 'partenaire' and conversation.partenaire_id != g.user.id:
            return jsonify({'error': 'Accès refusé'}), 403
        elif g.role in ['client', 'admin'] and conversation.client_id != g.user.id:
            return jsonify({'error': 'Accès refusé'}), 403
        
        # Créer le message
        message = Message(
            conversation_id=conversation_id,
            expediteur_type=g.role,
            contenu=contenu,
            type_message=type_message,
            date_envoi=datetime.utcnow()
        )
        
        if g.role == 'guest':
            message.expediteur_id = None
        else:
            message.expediteur_id = g.user.id
        
        # Mettre à jour la dernière activité de la conversation
        conversation.derniere_activite = datetime.utcnow()
        
        db.session.add(message)
        db.session.commit()
        
        return jsonify({
            'message': message.to_dict(),
            'success': 'Message envoyé avec succès'
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@chat_bp.route('/conversations/<conversation_id>/messages/<int:message_id>/read', methods=['PUT'])
@require_auth()
def mark_message_read(conversation_id, message_id):
    """Marquer un message comme lu"""
    try:
        message = Message.query.filter_by(
            id=message_id,
            conversation_id=conversation_id
        ).first()
        
        if not message:
            return jsonify({'error': 'Message introuvable'}), 404
        
        message.lu = True
        db.session.commit()
        
        return jsonify({'success': 'Message marqué comme lu'})
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@chat_bp.route('/conversations/<conversation_id>/archive', methods=['PUT'])
@require_auth()
def archive_conversation(conversation_id):
    """Archiver une conversation"""
    try:
        conversation = Conversation.query.get(conversation_id)
        if not conversation:
            return jsonify({'error': 'Conversation introuvable'}), 404
        
        # Vérifier les permissions
        if g.role == 'partenaire' and conversation.partenaire_id != g.user.id:
            return jsonify({'error': 'Accès refusé'}), 403
        elif g.role in ['client', 'admin'] and conversation.client_id != g.user.id:
            return jsonify({'error': 'Accès refusé'}), 403
        
        conversation.statut = 'archived'
        db.session.commit()
        
        return jsonify({'success': 'Conversation archivée'})
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@chat_bp.route('/unread-count', methods=['GET'])
@require_auth()
def get_unread_count():
    """Récupérer le nombre de messages non lus"""
    try:
        if g.role == 'partenaire':
            conversations = Conversation.query.filter_by(partenaire_id=g.user.id).all()
        elif g.role in ['client', 'admin']:
            conversations = Conversation.query.filter_by(client_id=g.user.id).all()
        else:
            return jsonify({'unread_count': 0})
        
        unread_count = 0
        for conv in conversations:
            unread_messages = Message.query.filter_by(
                conversation_id=conv.id,
                lu=False
            ).filter(Message.expediteur_id != g.user.id).count()
            unread_count += unread_messages
        
        return jsonify({'unread_count': unread_count})
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

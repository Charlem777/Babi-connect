# utils/jwt.py

import jwt
from datetime import datetime, timedelta
from backend.config import SECRET_KEY

def generate_token(id, role):
    payload = {
        'id': id,  # ✅ cohérent avec middleware
        'role': role,
        'exp': datetime.utcnow() + timedelta(days=1)
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')
    if isinstance(token, bytes):
        token = token.decode('utf-8')
    return token


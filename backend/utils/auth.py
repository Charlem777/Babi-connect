import jwt
import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from backend.config import SECRET_KEY

# 🔐 Génération du token JWT
def create_jwt_token(id, role="partenaire"):
    payload = {
        "id": id,  # ✅ cohérent avec g.user.id dans le middleware
        "role": role,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(days=1)
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")
    return token

# 🔍 Décodage du token JWT
def decode_jwt_token(token):
    try:
        return jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
    except jwt.ExpiredSignatureError:
        print("⏰ Token expiré")
        return None
    except jwt.InvalidTokenError as e:
        print("❌ Token invalide:", str(e))
        return None

# 🔐 Hash du mot de passe (pour seed ou création admin)
def hash_password(password):
    return generate_password_hash(password)

# 🔍 Vérification du mot de passe
def verify_password(hashed_password, plain_password):
    return check_password_hash(hashed_password, plain_password)

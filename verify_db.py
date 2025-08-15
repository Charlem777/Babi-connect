import os
from backend.extensions import db
from backend.models import Partenaire, Abonnement
from flask import Flask

app = Flask(__name__)

# Build absolute path to the DB
base_dir = os.path.abspath(os.path.dirname(__file__))
db_path = os.path.join(base_dir, 'instance', 'babi_connect.db')
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

with app.app_context():
    print("✅ DB URI:", app.config['SQLALCHEMY_DATABASE_URI'])
    try:
        print("🔍 Partenaires:", Partenaire.query.count())
        print("🔍 Abonnements:", Abonnement.query.count())
    except Exception as e:
        print("❌ Error accessing DB:", e)

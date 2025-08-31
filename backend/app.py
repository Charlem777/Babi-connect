from flask import Flask, jsonify, render_template   
from flask_cors import CORS
from flask_migrate import Migrate
from backend.extensions import db
from backend.routes.partenaire import partenaire_bp
from backend.api import api_bp
from backend.routes.offres import offres_bp
from backend.cli import seed_slugs, seed_tags
import os
from backend.routes.secteur import secteur_bp
from backend.routes.auth import auth_bp
from backend.routes.admin import admin_bp
from backend.routes.partenaire_interface import partenaireint_bp
from backend.routes.chat import chat_bp

base_dir = os.path.abspath(os.path.dirname(__file__))
db_path = os.path.join(base_dir, '..', 'instance', 'babi_connect.db')

def create_app():
    app = Flask(__name__, template_folder="../frontend", static_folder="static")
    CORS(
        app,
        resources={r"/api/*": {"origins": ["http://localhost:5173", "http://127.0.0.1:5173"]}},
        supports_credentials=True,
        allow_headers=["Content-Type", "Authorization", "X-Requested-With"],
        methods=["GET", "POST", "PUT", "DELETE", "OPTIONS", "HEAD"],
        expose_headers=["Content-Range", "X-Content-Range"]
    )

    app.cli.add_command(seed_tags)

    print(f"📁 DB path: {db_path}")
    app.cli.add_command(seed_slugs)

    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    app.register_blueprint(partenaire_bp, url_prefix='/api')
    app.register_blueprint(offres_bp, url_prefix='/api')
    app.register_blueprint(secteur_bp,url_prefix='/api')  # ← Enregistrement
    app.register_blueprint(auth_bp, url_prefix='/api')
    app.register_blueprint(admin_bp )  # ← ajoute cette ligne
    app.register_blueprint(partenaireint_bp, url_prefix='/api/partenaire')
    app.register_blueprint(chat_bp)  # Routes de chat

    print("📦 Registered routes:")
    for rule in app.url_map.iter_rules():
        print(rule)
    db.init_app(app)
    Migrate(app, db)
    app.register_blueprint(api_bp)

    print("🚀 Serveur Flask prêt à être lancé")
    return app

# Démarrage ici (hors de la fonction)
if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)

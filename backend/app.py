# backend/app.py

from flask import Flask, jsonify, render_template   
from flask_cors import CORS
from flask_migrate import Migrate
from backend.extensions import db
from backend.routes.partenaire import partenaire_bp
from backend.api import api_bp
from backend.routes.offres import offres_bp
from backend.cli import seed_slugs
import os
from backend.routes.secteur import secteur_bp

base_dir = os.path.abspath(os.path.dirname(__file__))
db_path = os.path.join(base_dir, '..', 'instance', 'babi_connect.db')

def create_app():
    app = Flask(__name__, template_folder="../frontend")
    print(f"📁 DB path: {db_path}")
    app.cli.add_command(seed_slugs)

    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    app.register_blueprint(partenaire_bp)
    app.register_blueprint(offres_bp, url_prefix='/api')
    app.register_blueprint(secteur_bp)  # ← Enregistrement

    print("📦 Registered routes:")
    for rule in app.url_map.iter_rules():
        print(rule)
    db.init_app(app)
    Migrate(app, db)
    CORS(app)
    app.register_blueprint(api_bp)

    print("🚀 Serveur Flask prêt à être lancé")
    return app

# Démarrage ici (hors de la fonction)
if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)

   

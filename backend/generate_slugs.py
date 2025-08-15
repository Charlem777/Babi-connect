import csv
import re
from models import Partenaire
from extensions import db
from flask import Flask

app = Flask(__name__)
app.config.from_object('config')  # adapte selon ton fichier config
db.init_app(app)

def slugify(text):
    text = text.lower()
    text = re.sub(r'[^\w\s-]', '', text)
    text = re.sub(r'[\s_-]+', '-', text)
    return text.strip('-')

with app.app_context():
    with open('partenaires.csv', newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            partenaire = Partenaire.query.get(int(row['id']))
            if partenaire:
                partenaire.url = slugify(row['nom'])
                print(f"✅ {row['nom']} → {partenaire.url}")
        db.session.commit()
    print("🎉 Slugs mis à jour avec succès.")

import os

class Config:
    SQLALCHEMY_DATABASE_URI = 'sqlite:///../plans.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'kobiri_secret'
# config.py
SECRET_KEY = "ton_secret_super_secure"

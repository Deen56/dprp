import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dprp-secret-key-2025'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///dprp.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
import os

class Config:
    SECRET_KEY =os.getenv('SECRET_KEY', 'your secrete key')
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL_v2', 'Your local url link')
    SQLALCHEMY_TRACK_MODIFICATIONS = False


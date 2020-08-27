import logging
import os
from dotenv import load_dotenv, find_dotenv
import secrets
from passlib.hash import bcrypt, pbkdf2_sha512
from zxcvbn import zxcvbn

load_dotenv(find_dotenv(), verbose=True, override=True)

# Discord 
CLIENT_ID = os.getenv('CLIENT_ID')
CLIENT_SECRET = os.getenv('CLIENT_SECRET')
API_BASE_URL = os.getenv('API_BASE_URL')
ACCESS_TOKEN_URL = os.getenv('ACCESS_TOKEN_URL')
AUTHORIZE_URL = os.getenv('AUTHORIZE_URL')
SCOPE = ['identify', 'email', 'guilds', 'guilds.join']
REDIRECT_URI = os.getenv('REDIRECT_URI')
TOKEN_URL = os.getenv('TOKEN_URL')

class Config:
    DEBUG = True
    TESTING = False

    @staticmethod
    def init_app(app):
        pass

class DevelopmentConfig(Config):
    DEBUG = True
    SECRET_KEY = os.getenv('SECRET_KEY')
    # database
    SQLALCHEMY_DATABASE_URI = 'sqlite:///../db.sqlite3'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # security
    SECURITY_LOGIN_URL = '/login'
    SECURITY_PASSWORD_SALT = 'thisisasecretsalt'

class TestingConfig(Config):
    TESTING = True
    # Database
    SQLALCHEMY_DATABASE_URI = 'sqlite:///../db.sqlite3'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # Security


class ProductionConfig(Config):
    DEBUG = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:///../db.sqlite3'

config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
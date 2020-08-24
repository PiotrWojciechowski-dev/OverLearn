import logging
import os
from dotenv import load_dotenv, find_dotenv
import secrets
from passlib.hash import bcrypt, pbkdf2_sha512
from zxcvbn import zxcvbn

load_dotenv(find_dotenv(), verbose=True, override=True)

name='discord'
client_id='745718221692469258'
client_secret='s2YbCr9Ks0ik4HbelwUDeg-UJ2GL6M-U'
api_base_url='https://discord.com/api'
userinfo_endpoint='https://discordapp.com/api/users/%40me'
access_token_url='https://discord.com/api/oauth2/token'
authorize_url='https://discord.com/api/oauth2/authorize'
redirect_uri = 'http://127.0.0.1:5000/authorize'
token_url = 'https://discordapp.com/api/oauth2/token'
scope = ['identify', 'email']

class Config:
    DEBUG = True
    TESTING = False

    @staticmethod
    def init_app(app):
        pass

class DevelopmentConfig(Config):
    DEBUG = True
    SECRET_KEY = os.getenv('SECRET_KEY')
    DISCORD_CLIENT_ID = '745718221692469258'
    DISCIRD_CLIENT_SECRETE = 's2YbCr9Ks0ik4HbelwUDeg-UJ2GL6M-U'
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
import logging
import os
from dotenv import load_dotenv, find_dotenv
import secrets
from passlib.hash import bcrypt, pbkdf2_sha512
from zxcvbn import zxcvbn

load_dotenv(find_dotenv())

class Config:
    DEBUG = True
    TESTING = False

    @staticmethod
    def init_app(app):
        pass

class DevelopmentConfig(Config):
    DEBUG = True
    SECRET_KEY = 'thisisasecret'
    # database
    SQLALCHEMY_DATABASE_URI = 'sqlite:///../db.sqlite3'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # security
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
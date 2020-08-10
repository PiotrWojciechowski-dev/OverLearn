import logging
import os
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

class Config:
    SECRET_KEY = 'a-not-so-secret-key-000-!!!'
    DEBUG = True
    TESTING = False

    @staticmethod
    def init_app(app):
        pass

class DevelopmentConfig(Config):
    DEBUG = True
    # database
    SQLALCHEMY_DATABASE_URI = 'sqlite:///../db.sqlite3'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///../db.sqlite3'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    WTF_CSRF_ENABLED = False

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
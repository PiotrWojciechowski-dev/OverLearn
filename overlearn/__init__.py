import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from overlearn import settings

db = SQLAlchemy()

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(settings.DevelopmentConfig)
    db.init_app(app)

    # import models to be created in the database
    from user.models import User

    with app.app_context():
        db.create_all()

    # import blueprints and register them
    from .views import home as home_bp
    app.register_blueprint(home_bp)
    from user import user as user_bp
    app.register_blueprint(user_bp)

    return app


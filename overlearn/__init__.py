import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///../db.sqlite3'
    db.init_app(app)

    from user.models import User

    with app.app_context():
        db.create_all()

    from user import user as user_bp
    app.register_blueprint(user_bp)

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('settings.py', silent=True)
    else:
        # Load the test config if passed in
        app.config.from_mapping(test_config)

    return app
from flask import Flask, url_for, session
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_security import Security, SQLAlchemyUserDatastore
from overlearn import settings

db = SQLAlchemy()
migrate = Migrate()
security = Security()

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(settings.DevelopmentConfig)

    # Initialize the database
    db.init_app(app)

    # Initialize Migrations
    migrate.init_app(app, db)

    # import User Model
    from overlearn.user.models import User, Role

    user_datastore = SQLAlchemyUserDatastore(db, User, Role)
    security.init_app(app, user_datastore)

    with app.app_context():
        db.create_all()

        # import blueprints and register them
        from .views import home as home_bp
        app.register_blueprint(home_bp)
        from overlearn.user import user as user_bp
        app.register_blueprint(user_bp)

    return app


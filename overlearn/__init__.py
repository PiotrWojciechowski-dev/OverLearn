from flask import Flask, url_for, session
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from flask_migrate import Migrate
from flask_security import Security, SQLAlchemyUserDatastore
from overlearn import settings

db = SQLAlchemy()
migrate = Migrate()
security = Security()

convention = {
    "ix": 'ix_%(column_0_label)s',
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
}

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(settings.DevelopmentConfig)

    # Initialize the database
    #metadata = MetaData(naming_convention=convention)
    #db = SQLAlchemy(app, metadata=metadata)
    db.init_app(app)

    # Initialize Migrations
    migrate.init_app(app, db, render_as_batch=True)

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

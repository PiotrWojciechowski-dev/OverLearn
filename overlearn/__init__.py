from flask import Flask, url_for, session
from overlearn import settings
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_oauthlib.provider import OAuth2Provider
from flask_security import ( Security, SQLAlchemyUserDatastore,
                            AnonymousUser )
from flask_security.core import (
    _user_loader as _flask_security_user_loader,
    _request_loader as _flask_security_request_loader)
from flask_security.utils import config_value as security_config_value

db = SQLAlchemy()
migrate = Migrate()
security = Security()
login_manager = LoginManager()
oauth = OAuth2Provider()

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
    security.init_app(app, user_datastore, login_manager=_get_login_manager(app, anonymous_user=None))

    with app.app_context():
        db.create_all()

        # import blueprints and register them
        from .views import home as home_bp
        app.register_blueprint(home_bp)
        from overlearn.user import user as user_bp
        app.register_blueprint(user_bp)

    return app

def _request_loader(request):
    """
    Load user from OAuth2 Authentication header or using
    Flask-Security's request loader.
    """
    user = None
    # if header attribute has oauth login user using supported oauth 
    if hasattr(request, 'oauth'):
        user = request.oauth.user
    else:
        # Need this try stmt in case oauthlib sometimes throws:
        # AttributeError: dict object has no attribute startswith
        try:
            is_valid, oauth_request = oauth.verify_request(scopes=[])
            if is_valid:
                user = oauth_request.user
        except AttributeError:
            pass

    if not user:
        user = _flask_security_request_loader(request)

    return user

def _get_login_manager(app, anonymous_user):
    """Prepare a login manager for Flask-Security to use."""
    login_manager.anonymous_user = anonymous_user or AnonymousUser
    # BLUEPRINT_NAME in flask_security is missing so hardcode whatever blueprint login is set to
    login_manager.login_view = 'security.login'
    login_manager.user_loader(_flask_security_user_loader)
    login_manager.request_loader(_request_loader)

    if security_config_value('FLASH_MESSAGES', app=app):
        (login_manager.login_message,
         login_manager.login_message_category) = (
            security_config_value('MSG_LOGIN', app=app))
        (login_manager.needs_refresh_message,
         login_manager.needs_refresh_message_category) = (
            security_config_value('MSG_REFRESH', app=app))
    else:
        login_manager.login_message = None
        login_manager.needs_refresh_message = None

    login_manager.init_app(app)
    return login_manager



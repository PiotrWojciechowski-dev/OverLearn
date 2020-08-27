from flask import ( Flask, render_template, request,
                redirect, url_for, current_app, session )
from flask_login import current_user, login_required, login_user
from . import user
from .models import User
from .forms import RegistrationForm
from overlearn import db, security, oauth, settings
from flask_security.utils import hash_password
from flask_security import ( anonymous_user_required, 
                            LoginForm, url_for_security )
from authlib.integrations.requests_client import OAuth2Session
import secrets

@user.route('/register', methods=('GET', 'POST'))
@anonymous_user_required
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        security.datastore.create_user(
            username=request.form['username'],
            email=request.form['email'],
            password=hash_password(request.form['password']),
        )
        db.session.commit()
        return redirect((url_for('user.profile', username=current_user)))
    return render_template('user/register.html', form=form)

@user.context_processor
def login_context():
    return {
        'url_for_security': url_for_security,
        'login_user_form': LoginForm(),
    }

@user.route('/logins')
def login():
    oauth = OAuth2Session(settings.CLIENT_ID, redirect_uri=settings.REDIRECT_URI, scope=settings.SCOPE, client_secret=settings.CLIENT_SECRET)
    login_url, state = oauth.create_authorization_url(settings.AUTHORIZE_URL)
    session['state'] = state
    return render_template('security/login_user.html', login_url=login_url)

@user.route('/authorize')
def authorize():
    discord = OAuth2Session(settings.CLIENT_ID, redirect_uri=settings.REDIRECT_URI, scope=settings.SCOPE, client_secret=settings.CLIENT_SECRET)
    token = discord.fetch_token(
        settings.TOKEN_URL,
        client_secret=settings.CLIENT_SECRET,
        authorization_response=request.url,
    )
    # set token to session and create a user using the API
    session['discord_token'] = token
    response = discord.get(settings.API_BASE_URL + '/users/@me')
    discord_user = response.json()
    user = User.query.filter_by(email=discord_user['email']).first()
    if not user:
        user = User(
            username=discord_user['username'],
            password=hash_password(secrets.token_urlsafe()),
            email=discord_user['email'],
            active=True,
        )
        db.session.add(user)
        db.session.commit()
    login_user(user, True)
    return redirect((url_for('user.profile', username=discord_user['username'])))

@user.route('/profile/<username>', methods=('GET', 'POST'))
@login_required
def profile(username):
    user = current_user
    guild_id = '747478996513456129'
    discord = OAuth2Session(settings.CLIENT_ID, token=session['discord_token'])
    response = discord.get(settings.API_BASE_URL + '/users/@me')
    return render_template('user/profile.html', user=user, response=response.json())
from flask import ( Flask, render_template, request,
                redirect, url_for, current_app, session )
from flask_login import current_user, login_required, login_user
from . import user
from .models import User
from .forms import RegistrationForm
from overlearn import db, security, oauth, settings
from flask_security.utils import hash_password
from flask_security import anonymous_user_required, LoginForm, url_for_security
from authlib.integrations.requests_client import OAuth2Session

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

@user.route('/login')
def login():
    oauth = OAuth2Session(settings.client_id, redirect_uri=settings.redirect_uri, scope=settings.scope, client_secret=settings.client_secret)
    login_url, state = oauth.create_authorization_url(settings.authorize_url)
    session['state'] = state
    return render_template('security/login_user.html', login_url=login_url)
'''
@user.route('/discord_login')
def discord_login():
    redirect_uri = url_for('user.authorize', _external=True)
    return oauth.discord.authorize_redirect(redirect_uri)
'''
@user.route('/authorize')
def authorize():
    discord = OAuth2Session(settings.client_id, redirect_uri=settings.redirect_uri, state=session['state'], scope=settings.scope)
    token = discord.fetch_token(
        settings.token_url,
        client_secret=settings.client_secret,
        authorization_response=request.url,
    )
    session['discord_token'] = token
    print(session)
    # do something with the token and profile

    #return redirect((url_for('user.profile', username=username)))
    return redirect((url_for('home.index')))

@user.route('/profile/<username>', methods=('GET', 'POST'))
@login_required
def profile(username):
    user = current_user
    token = oauth.discord.request()
    print(token)
    response = 'https://discord.com/api' + '/users/@me'
    return render_template('user/profile.html', user=user, response=response)
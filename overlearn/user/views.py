from flask import Flask, render_template, request, redirect, url_for, current_app
from flask_login import current_user, login_required, login_user
from . import user
from .models import User
from .forms import RegistrationForm
from overlearn import db, security
from flask_security.utils import hash_password
from flask_security import anonymous_user_required


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

@user.route('/profile/<username>', methods=('GET', 'POST'))
@login_required
def profile(username):
    user = current_user
    return render_template('user/profile.html', user=user)

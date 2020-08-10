from flask import Flask, render_template, request, redirect, url_for
from . import user
from .models import User
from .forms import RegistrationForm
from overlearn import db

@user.route('/user/register', methods=('GET', 'POST'))
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        new_user = User(
            username=request.form['username'],
            email=request.form['email'],
            password=request.form['password'],
        )
        db.session.add(new_user)
        db.session.commit()
        return redirect('/')
    return render_template('/user/register.html', form=form)

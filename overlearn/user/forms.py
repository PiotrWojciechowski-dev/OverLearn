from flask import request
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, validators
from wtforms.validators import InputRequired
from wtforms.fields.html5 import EmailField
from .models import User
from sqlalchemy import or_

style={'class': 'form-row form-group form-control mb-3 w-25'}

class RegistrationForm(FlaskForm):
    """
    Register a User
    """
    username = StringField('Name: ', validators=[InputRequired()],render_kw=style)
    email = EmailField('Email: ', validators=[InputRequired()],render_kw=style)
    password = PasswordField('Password: ', validators=[InputRequired()],render_kw=style) 
'''
class LogInForm(FlaskForm):
    username = StringField('Username: ', validators=[InputRequired()],render_kw=style)
    email = StringField('Email: ', validators=[InputRequired()],render_kw=style)
    password = PasswordField('Password: ', validators=[InputRequired()],render_kw=style)
'''
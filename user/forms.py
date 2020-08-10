from flask_wtf import FlaskForm
from wtforms import StringField, validators
from wtforms.validators import InputRequired
from wtforms.fields.html5 import EmailField

class RegistrationForm(FlaskForm):
    """
    Register a User
    """
    username = StringField('Name: ', validators=[InputRequired()])
    email = EmailField('Email: ', validators=[InputRequired()])
    password = StringField('Password: ', validators=[InputRequired()]) 
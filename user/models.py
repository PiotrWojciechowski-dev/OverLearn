from flask_sqlalchemy import SQLAlchemy
from overlearn import db

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(15), unique=True)
    password = db.Column(db.String(30))
    email = db.Column(db.String(120), unique=True)

    def __init__(self, username=None, email=None, password=None):
        self.username = username
        self.email = email
        self.password = password
    
    def __repr__(self):
        return '<User %r' % (self.username)

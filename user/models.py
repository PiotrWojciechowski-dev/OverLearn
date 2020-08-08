from flask_sqlalchemy import SQLAlchemy
from overlearn import db

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(15), unique=True)
    email = db.Column(db.String(120), unique=True)

    def __init__(self, name=None, email=None):
        self.name = name
        self.email = email
    
    def __repr__(self):
        return '<User %r' % (self.name)

from flask import Blueprint, render_template, request
from user.models import User
from overlearn import create_app, db

home = Blueprint('home', __name__,  template_folder='../templates')

@home.route('/', methods=['GET', 'POST'])
def index():
    username = request.authorization
    user = User.query.all()
    #user = User.query.filter_by(username=username).first_or_404()
    return render_template('home/home.html', user=user)
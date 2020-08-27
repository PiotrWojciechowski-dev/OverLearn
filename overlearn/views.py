from flask import Blueprint, render_template, request, \
current_app, url_for, session
from overlearn.user.models import User
from overlearn import create_app, db
from flask_login import current_user

home = Blueprint('home', __name__,  template_folder='../templates')

@home.route('/', methods=['GET', 'POST'])
def index():
    user = current_user
    print(session)
    #user = User.query.filter_by(username=username).first_or_404()
    return render_template('home/home.html', user=user)

def has_no_empty_params(rule):
        defaults = rule.defaults if rule.defaults is not None else ()
        arguments = rule.arguments if rule.arguments is not None else ()
        return len(defaults) >= len(arguments)

@home.route("/site")
def site_map():
    import json
    links = []
    for rule in current_app.url_map.iter_rules():
        # Filter out rules we can't navigate to in a browser
        # and rules that require parameters
        if "GET" in rule.methods and has_no_empty_params(rule):
            url = url_for(rule.endpoint, **(rule.defaults or {}))
            links.append((url, rule.endpoint))
    # links is now a list of url, endpoint tuples
    return json.dumps(links)
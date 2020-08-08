from flask import Flask, render_template
from . import user
app = Flask(__name__,)

@user.route('/')
def hello_world():
    return render_template("base.html")

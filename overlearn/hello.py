from flask import Flask, render_template
#url_for('static', filename='overlearn.css')
app = Flask(__name__, static_folder='')

@app.route('/')
def hello_world():
    return render_template("base.html")


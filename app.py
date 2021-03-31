from flask import Flask, render_template, Blueprint
from flask_sqlalchemy import SQLAlchemy
from project.model import db

app = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# app.register_blueprint(bp_docent)
# https://flask.palletsprojects.com/en/1.1.x/blueprints/

db.init_app(app)

@app.route('/')
def index():
    return render_template('home.html')

if __name__ == "__main__":
    app.run()
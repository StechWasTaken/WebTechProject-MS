import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from project.studenten.views import studenten_blueprint

app = Flask(__name__)

app.config['SECRET_KEY'] = 'mijngeheimesleutel'

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.register_blueprint(studenten_blueprint, url_prefix="/studenten")

import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask.blueprints import Blueprint
from project.models import *


# de app moet hier geïnitialiseerd worden, niet in app.py, hier pakt hij __name__ goed
app = Flask(__name__)

app.config['SECRET_KEY'] = 'mijngeheimesleutel'

# Database
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.create_all()

# Blueprints
from project.studenten.views import studenten_blueprint
from project.views import standaard_blueprint

app.register_blueprint(studenten_blueprint, url_prefix="/studenten")
app.register_blueprint(standaard_blueprint)


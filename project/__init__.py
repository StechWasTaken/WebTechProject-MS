import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask.blueprints import Blueprint
from flask_user import current_user, login_required, roles_required, UserManager, UserMixin
from project.models import *

# de app moet hier geïnitialiseerd worden, niet in app.py, hier pakt hij __name__ goed
app = Flask(__name__)

app.config['SECRET_KEY'] = 'mijngeheimesleutel'

# Database
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
migrate.init_app(app, db)
login_manager.init_app(app)
login_manager.login_view = 'standaard.login'

with app.app_context():
    db.create_all()
 

# Blueprints
from project.gebruikers.student.views import student_blueprint
from project.views import standaard_blueprint

app.register_blueprint(student_blueprint, url_prefix="/student")
app.register_blueprint(standaard_blueprint)



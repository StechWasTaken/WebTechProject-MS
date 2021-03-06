import os
from datetime import datetime, timedelta, time
from calendar import *
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask.blueprints import Blueprint
from project.models import *
from flask_login import current_user

# de app moet hier geïnitialiseerd worden, niet in app.py, hier pakt hij __name__ goed
app = Flask(__name__)

@app.context_processor
def inject_time_related_functions():
    """ Geeft global variabelen mee aan alle templates, zodat deze gebruikt kunnen worden.
    """
    return dict(date_now=datetime.now().date(), td=timedelta, dt=datetime, t=time())

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
    try:
        student = Role(name='student')
        docent = Role(name='docent')
        admin = Role(name='admin')
        db.session.add(student)
        db.session.add(docent)
        db.session.add(admin)
        db.session.commit()
    except:
        print('roles already exist')
 
# Blueprints
from project.gebruikers.student.views import student_blueprint
from project.gebruikers.admin.views import admin_blueprint
from project.gebruikers.docent.views import docent_blueprint
from project.views import standaard_blueprint

app.register_blueprint(student_blueprint, url_prefix="/student")
app.register_blueprint(standaard_blueprint)
app.register_blueprint(admin_blueprint, url_prefix="/admin")
app.register_blueprint(docent_blueprint, url_prefix="/docent")

from flask import render_template
from flask.blueprints import Blueprint
# from project import db

standaard_blueprint = Blueprint('standaard',
                             __name__,
                             template_folder='templates')

@standaard_blueprint.route('/cursus')
def cursus():
    # code voor cursus

    return render_template('cursus.html',)
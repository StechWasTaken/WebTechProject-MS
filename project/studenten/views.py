from flask import render_template
from flask.blueprints import Blueprint
# from project import db
# from project.model import Rooster

studenten_blueprint = Blueprint('studenten',
                             __name__,
                             template_folder='templates/studenten')

@studenten_blueprint.route('/rooster')
def rooster():
    # code voor rooster

    return render_template('rooster.html',)
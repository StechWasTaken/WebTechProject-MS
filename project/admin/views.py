from flask import render_template
from flask.blueprints import Blueprint
# from project import db
# from project.model import Rooster

# rooster, cursussen en talen toevoegen, docentgegevens bewerken

admin_blueprint = Blueprint('admin',
                             __name__,
                             template_folder='templates/admin')

@admin_blueprint.route('/rooster')
def rooster():
    # code voor rooster

    return render_template('rooster.html')
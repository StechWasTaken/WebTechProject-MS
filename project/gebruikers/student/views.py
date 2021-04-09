from flask import render_template
from flask.blueprints import Blueprint
from project.roles import role_required
# from project import db
# from project.model import Rooster

student_blueprint = Blueprint('student',
                             __name__,
                             template_folder='templates/student')

@student_blueprint.route('/student/rooster')
@role_required('student')
def rooster():
    # code voor rooster

    return render_template('rooster.html',)
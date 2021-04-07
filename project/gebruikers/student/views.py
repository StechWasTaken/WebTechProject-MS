from flask.blueprints import Blueprint
from flask import render_template, flash, redirect, url_for, Markup
from flask.blueprints import Blueprint
from flask_login import login_user, login_required, logout_user, current_user
from project.models import *
from project import *

student_blueprint = Blueprint('student',
                             __name__,
                             template_folder='templates/student')

@student_blueprint.route('/inschrijvingen/<username>')
@login_required
def inschrijvingen(username):
    if username != current_user.username:
        return redirect(url_for('index'))

    inschrijvingen =    Attendee.query\
                        .filter_by(user_id=current_user.id)\
                        .join(Lecture, Lecture.id == Attendee.lecture_id)\
                        .join(Teacher, Teacher.id == Lecture.teacher_id)\
                        .join(Language, Language.id == Lecture.language_id)\
                        .add_columns(Lecture.id, Language.language, Teacher.username, Lecture.start_time, Lecture.location)

    return render_template('inschrijvingen.html', inschrijvingen=inschrijvingen)

@student_blueprint.route('/inschrijven/<language_id>/<lecture_id>')
@login_required
def inschrijven(language_id, lecture_id):
    language = Language.query.filter_by(id=language_id).first()
    if Attendee.query.filter_by(user_id=current_user.id, lecture_id=int(lecture_id)).first() == None:
        try:
            attendee = Attendee(user_id=current_user.id, lecture_id=int(lecture_id))
            db.session.add(attendee)
            db.session.commit()
        except:
            flash('Inschrijven mislukt.')
            return redirect(url_for('standaard.cursus', language=language, lecture_id=lecture_id))
    else:
        flash('Inschrijven mislukt.')
        return redirect(url_for('standaard.cursus', language=language, lecture_id=lecture_id))
    return redirect(url_for('student.inschrijvingen', username=current_user.username))
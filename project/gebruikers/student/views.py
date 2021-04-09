from flask.blueprints import Blueprint
from project.roles import *
# from project import db
# from project.model import Rooster
from flask import render_template, flash, redirect, url_for, Markup
from flask.blueprints import Blueprint
from flask_login import login_user, login_required, logout_user, current_user
from project.models import *
from project import *
from .forms import *

student_blueprint = Blueprint('student',
                             __name__,
                             template_folder='templates/student')

@student_blueprint.route('/rooster')
@role_required('student')
def rooster():
    # code voor rooster
    return
    
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

@student_blueprint.route('/instellingen', methods=['GET', 'POST'])
@login_required
def instellingen():
    user = User.query.filter_by(id=current_user.id).first()
    
    username_form = AlterUsernameForm()
    email_form = AlterEmailForm()
    password_form = AlterPasswordForm()

    if username_form.validate_on_submit():
        flash('username changed')
    if email_form.validate_on_submit():
        flash('email changed')
    if password_form.validate_on_submit():
        flash('password changed')

    return render_template('instellingen.html', username_form=username_form, email_form=email_form, password_form=password_form) 
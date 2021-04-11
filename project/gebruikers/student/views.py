from datetime import *
from calendar import *
import locale
from flask.blueprints import Blueprint
from project.roles import *
from flask import render_template, flash, redirect, url_for, Markup
from flask.blueprints import Blueprint
from flask_login import login_user, login_required, logout_user, current_user
from project.models import *
from project import *
from .forms import *

student_blueprint = Blueprint('student',
                             __name__,
                             template_folder='templates/student')

@student_blueprint.route('/rooster/<year>/<week>')
@role_required('student')
def rooster(year, week):
    locale.setlocale(locale.LC_TIME, 'nl_NL.utf8')
    calendar = Calendar()
    current_year = int(year)
    current_week = int(week)
    current_day = datetime.now().date()

    dates = []
    for month in range(1, 13):
        month_dates = calendar.monthdatescalendar(current_year, month)
        for week_dates in month_dates:
            for date in week_dates:
                if date.isocalendar()[1] == current_week:
                    if date not in dates:
                        dates.append(date)

    if current_week-1 < 1:
        previous = (current_year-1, 52)
    else:
        previous = (current_year, current_week-1)
    
    if current_week+1 > 52:
        next = (current_year+1, 1)
    else:
        next = (current_year, current_week+1)

    return render_template('rooster.html', dates=dates, current_day=current_day, previous=previous, next=next)
    
@student_blueprint.route('/inschrijvingen/<username>')
@login_required
def inschrijvingen(username):
    """ Kijkt bij welke cursussen de gebruiker is ingeschreven
    Ook berekent hij de korting hier
    """
    korting = Korting()

    if username != current_user.username:
        return redirect(url_for('index'))

    inschrijvingen =    Attendee.query\
                        .filter_by(user_id=current_user.id)\
                        .join(Course, Course.id == Attendee.course_id)\
                        .join(User, User.id == Course.teacher_id)\
                        .join(Language, Language.id == Course.language_id)\
                        .add_columns(Course.id, Language.language, User.username, Course.location, Course.cost, Attendee.discount)

    return render_template('inschrijvingen.html', inschrijvingen=inschrijvingen, korting=korting)

@student_blueprint.route('/inschrijven/<language_id>/<course_id>')
@login_required
def inschrijven(language_id, course_id):
    language = Language.query.filter_by(id=language_id).first()
    if Attendee.query.filter_by(user_id=current_user.id, course_id=int(course_id)).first() == None:
        discount = False
        if Attendee.query.filter_by(user_id=current_user.id).first() != None: # Als de user al een keer is ingeschreven krijgt hij korting
            discount = True
        try:
            attendee = Attendee(user_id=current_user.id, course_id=int(course_id), discount=discount)
            db.session.add(attendee)
            db.session.commit()
        except:
            flash('Inschrijven mislukt.')
            return redirect(url_for('standaard.cursus', language=language, course_id=course_id))
    else:
        flash('U bent al ingeschreven voor deze cursus.')
        return redirect(url_for('standaard.cursus', language=language, course_id=course_id))
    return redirect(url_for('student.inschrijvingen', username=current_user.username))

@student_blueprint.route('/instellingen', methods=['GET', 'POST'])
@login_required
def instellingen():
    username_form = AlterUsernameForm()
    email_form = AlterEmailForm()
    password_form = AlterPasswordForm()

    user = User.query.filter_by(id=int(current_user.id)).first()

    if username_form.validate_on_submit():
        username = User.query.filter_by(username=username_form.username.data).first()
        if username == None:
            flash('Gebruikersnaam veranderd.')
            user.username = username_form.username.data
            db.session.commit()
        else:
            flash('Gebruikersnaam is al in gebruik.')
    if email_form.validate_on_submit():
        email = User.query.filter_by(email=email_form.email.data).first()
        if email == None:
            flash('Email veranderd.')
            user.email = email_form.email.data
            db.session.commit()
        else:
            flash('Email is al in gebruik.')
    if password_form.validate_on_submit():
        if user.check_password(password_form.old_password):
            flash('Wachtwoord veranderd.')
            user.password = password_form.new_password.data
            db.session.commit()
        else:
            flash('Huidige wachtwoord is incorrect.')

    return render_template('instellingen.html', username_form=username_form, email_form=email_form, password_form=password_form) 
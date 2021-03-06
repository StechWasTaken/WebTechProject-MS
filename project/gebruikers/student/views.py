from datetime import *
from calendar import *
import locale
from flask.blueprints import Blueprint
from project.roles import *
from flask import render_template, flash, redirect, url_for, Markup, request
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
    """ Rooster met alle lessen die student X volgt voor het meegegeven jaar en de meegegeven week.
    """
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

    start_date = dates[0]
    end_date = dates[len(dates)-1] + timedelta(days=1)

    student = db.session.query(User.id).filter(User.id == current_user.id).subquery('student')
    lectures =  Lecture.query\
                .join(Course, Course.id == Lecture.course_id)\
                .join(Attendee, Attendee.course_id == Course.id)\
                .join(Language, Language.id == Course.language_id)\
                .join(User, User.id == Course.teacher_id)\
                .join(student, student.c.id == Attendee.user_id)\
                .add_columns(Lecture.id, Language.language, User.username, Lecture.start_time, Lecture.end_time, Lecture.lecture_name)\
                .filter(Lecture.start_time >= start_date, Lecture.start_time < end_date)\
                .all()

    if current_week-1 < 1:
        if datetime(current_year-1, 12, 28).isocalendar()[1] == 53:
            previous = (current_year-1, 53)
        else:
            previous = (current_year-1, 52)
    else:
        previous = (current_year, current_week-1)
    
    if current_week+1 > 52:
        if datetime(current_year, 12, 28).isocalendar()[1] == 53 and current_week != 53:
            next = (current_year, 53)
        else:
            next = (current_year+1, 1)
    else:
        next = (current_year, current_week+1)

    return render_template('rooster.html', dates=dates, current_day=current_day, previous=previous, next=next, lectures=lectures)
    
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
    """ Schrijft gebruiker X in bij de gespecificeerde cursus.
    """
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
    """ Geeft de instellingen van gebruiker X weer en biedt de mogelijkheid om deze aan te passen.
    """
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
        if user.check_password(password_form.old_password.data):
            flash('Wachtwoord veranderd.')
            user.password = password_form.new_password.data
            db.session.commit()
        else:
            flash('Huidige wachtwoord is incorrect.')
    elif request.method == 'POST':
        flash('validate mislukt')

    return render_template('instellingen.html', username_form=username_form, email_form=email_form, password_form=password_form) 
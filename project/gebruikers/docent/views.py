import locale
from datetime import *
from calendar import *
from flask import current_app, flash, redirect, render_template
from flask.blueprints import Blueprint
from flask_login import current_user
from project.models import *
from project import app
from project.roles import *
from project.gebruikers.admin.forms import *

# /admin

docent_blueprint = Blueprint('docent', __name__, template_folder='templates/docent')

@docent_blueprint.route('/rooster/<year>/<week>')
@role_required('docent')
def docent_rooster(year, week):
    """ Rooster met alle lessen die docent X moet geven voor het meegegeven jaar en de meegegeven week.
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

    docent = db.session.query(User.id).filter(User.id == current_user.id).subquery('docent')
    lectures =  Lecture.query\
                .join(Course, Course.id == Lecture.course_id)\
                .join(Language, Language.id == Course.language_id)\
                .join(User, User.id == Course.teacher_id)\
                .join(docent, docent.c.id == Course.teacher_id)\
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

    return render_template('docent_rooster.html', dates=dates, current_day=current_day, previous=previous, next=next, lectures=lectures)
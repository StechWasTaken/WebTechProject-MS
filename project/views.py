from flask import render_template, flash, redirect, url_for, Markup, request, make_response
from flask.blueprints import Blueprint
from flask_login import login_user, login_required, logout_user, current_user
from project.forms import *
from project.models import *
from project import app
from project.roles import *

standaard_blueprint = Blueprint('standaard',
                             __name__,
                             template_folder='templates')

@standaard_blueprint.route('/cursussen')
def cursussen():
    """ Geeft alle cursussen weer.
    """
    courses =  Course.query\
                .join(Language, Course.language_id == Language.id)\
                .join(User, Course.teacher_id == User.id)\
                .add_columns(Course.id, Language.language, User.username, Course.location)

    return render_template('cursussen.html', courses=courses)

@standaard_blueprint.route('/cursus/<language>/<course_id>')
def cursus(language, course_id):
    """ laad de cursuspagina van de taal samen met de course id
    haalt deze uit de database
    """
    if current_user.is_anonymous:
        flash(Markup('U moet eerst inloggen of registreren voordat u zich kan inschrijven voor een cursus. <br> Registreren kan <b><a href="' + url_for('standaard.register') + '">hier</a></b>! <br><br> <b><a href="' + url_for('standaard.login') + '">Inloggen</a></b>'))

    course =   Course.query\
                .filter_by(id=course_id)\
                .join(Language, Course.language_id == Language.id)\
                .join(User, Course.teacher_id == User.id)\
                .add_columns(Course.id, Course.language_id, Language.language, User.username, Course.location, Course.cost, Course.description).first_or_404()
    
    lectures =  Lecture.query\
                .filter_by(course_id = int(course_id))\
                .join(Course, Course.id == int(course_id))\
                .join(Language, Language.id == Course.language_id)\
                .add_columns(Lecture.lecture_name, Lecture.start_time, Lecture.end_time)\
                .order_by(Lecture.start_time)\
                .all()

    # kijkt naar discount
    discount = False
    korting = Korting()
    if current_user.is_authenticated:
        if Attendee.query.filter_by(user_id = current_user.id).first() != None:
            discount = True

    return render_template('cursus.html', course=course, discount = discount, korting=korting, lectures=lectures)

@standaard_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    """ Laad de login pagina en logt gebruiker X in wanneer het formulier wordt ingediend.
        Kan ook terugverwijzen naar een pagina voor het inloggen door middel van een cookie.
    """
    # code voor login
    form = LoginForm()

    if request.method != 'POST':    # toch maar de try en except gebruikt ipv !='GET', want anders gaat hij nooit verder
        try:
            resp = make_response(render_template('login.html', form=form))
            resp.set_cookie('referrer', request.headers.get("Referer"))
            return resp
        except:
            print("cookie exception")

    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        try:
            if user.check_password(form.password.data) and user is not None:
                referrer = request.cookies.get('referrer')
                login_user(user)
                flash('Succesvol ingelogd.')
                if referrer is not None:
                    return redirect(referrer)
                return redirect(url_for('standaard.login'))
        except:
            flash('Inloggen mislukt.')
            return redirect(url_for('standaard.login'))

    return render_template('login.html', form=form)

@standaard_blueprint.route('/logout')
@login_required
def logout():
    """ logt gebruiker X uit.
    """
    logout_user()
    flash('Je bent nu uitgelogd!')
    return redirect(url_for('index'))

@standaard_blueprint.route('/register', methods=['GET', 'POST'])
def register():
    """ Laad de register pagina en registreert gebruiker X wanneer het formulier wordt ingediend.
    """
    # code voor register
    form = RegisterForm()

    if form.validate_on_submit():
        user = User(email=form.email.data,
                    username=form.username.data,
                    password=form.password.data,
                    role_id=1)

        db.session.add(user)
        db.session.commit()
        flash('Dank voor de registratie. Er kan nu ingelogd worden! ')

        return redirect(url_for('standaard.login'))

    return render_template('register.html', form=form)

 
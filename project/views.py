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
    # code voor cursus
    lectures =  Lecture.query\
                .join(Language, Lecture.language_id == Language.id)\
                .join(Teacher, Lecture.teacher_id == Teacher.id)\
                .add_columns(Lecture.id, Language.language, Teacher.username, Lecture.start_time, Lecture.location)

    return render_template('cursussen.html', lectures=lectures)

@standaard_blueprint.route('/cursus/<language>/<lecture_id>')
def cursus(language, lecture_id):
    if current_user.is_anonymous:
        flash(Markup('U moet eerst inloggen of registreren voordat u zich kan inschrijven voor een cursus. <br> Registreren kan <b><a href="' + url_for('standaard.register') + '">hier</a></b>! <br><br> <b><a href="' + url_for('standaard.login') + '">Inloggen</a></b>'))

    lecture =   Lecture.query\
                .filter_by(id=lecture_id)\
                .join(Language, Lecture.language_id == Language.id)\
                .join(Teacher, Lecture.teacher_id == Teacher.id)\
                .add_columns(Lecture.id, Lecture.language_id, Language.language, Teacher.username, Lecture.start_time, Lecture.location).first_or_404()
    
    return render_template('cursus.html', lecture=lecture)

@standaard_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    # code voor login
    form = LoginForm()

    if request.method != 'POST' and request.method != 'GET':
        resp = make_response(render_template('login.html', form=form))
        resp.set_cookie('referrer', request.headers.get("Referer"))
        return resp

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
    logout_user()
    flash('Je bent nu uitgelogd!')
    return redirect(url_for('index'))

@standaard_blueprint.route('/register', methods=['GET', 'POST'])
def register():
    # code voor register
    form = RegisterForm()

    if form.validate_on_submit():
        user = User(email=form.email.data,
                    username=form.username.data,
                    password=form.password.data)

        db.session.add(user)
        db.session.commit()
        flash('Dank voor de registratie. Er kan nu ingelogd worden! ')

        # student role toevoegen
        user = User.query.filter_by(email=form.email.data).first()
        addRole(user.id, 'student')

        return redirect(url_for('standaard.login'))

    return render_template('register.html', form=form)

 
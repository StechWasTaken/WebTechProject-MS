from flask import render_template, flash, redirect, url_for
from flask.blueprints import Blueprint
from flask_login import login_user, login_required, logout_user
from project.forms import *
from project.models import *
from project import app

standaard_blueprint = Blueprint('standaard',
                             __name__,
                             template_folder='templates')

@standaard_blueprint.route('/cursus')
def cursus():
    # code voor cursus
    lectures =  Lecture.query\
                .join(Language, Lecture.language_id == Language.id)\
                .join(Teacher, Lecture.teacher_id == Teacher.id)\
                .add_columns(Language.language, Teacher.username, Lecture.start_time, Lecture.location)

    return render_template('cursus.html', lectures=lectures)

@standaard_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    # code voor login
    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        print(user, user.check_password(form.password.data))
        if user.check_password(form.password.data) and user is not None:
            login_user(user)
            flash('Succesvol ingelogd.')
            return redirect(url_for('index'))

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

        #role toevoegen
        user = User.query.filter_by(email=form.email.data).first()
        addRole(user.id, 'student')

        return redirect(url_for('standaard.login'))

    return render_template('register.html', form=form)

 
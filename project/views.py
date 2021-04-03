from flask import render_template
from flask.blueprints import Blueprint
from project.forms import *
# from project import db

standaard_blueprint = Blueprint('standaard',
                             __name__,
                             template_folder='templates')

@standaard_blueprint.route('/cursus')
def cursus():
    # code voor cursus

    return render_template('cursus.html')

@standaard_blueprint.route('/login')
def login():
    # code voor login

    return render_template('login.html')

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

        return redirect(url_for('index')) # aanpassen!

    return render_template('register.html', form=form)

 
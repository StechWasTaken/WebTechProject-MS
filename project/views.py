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
    form = VoegtoeForm()

    if form.validate_on_submit():
        naam = form.naam.data

        new_cur = Cursist(naam)
        db.session.add(new_cur)
        db.session.commit()

        return redirect(url_for('index')) # aanpassen!

    return render_template('register.html')

 
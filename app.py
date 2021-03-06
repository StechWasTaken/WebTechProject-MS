import os
from project import app
from flask import Flask, render_template, Blueprint
from flask_sqlalchemy import SQLAlchemy
from project.models import *
from flask_login import current_user
from project.roles import *


# app.register_blueprint(bp_docent)
# https://flask.palletsprojects.com/en/1.1.x/blueprints/


@app.route('/')
def index():
    role = ''
    name = ''
    if current_user.is_authenticated:
        role = getRole(current_user.id)
        name = current_user.username

    # voor de cursus carousel
    cursussen = Course.query\
                .filter_by()\
                .join(Language, Course.language_id == Language.id)\
                .add_columns(Language.language, Course.description, Course.id).all()

    return render_template('home.html', role = role, name = name, cursussen=cursussen)

if __name__ == "__main__":
    app.run(debug=True)

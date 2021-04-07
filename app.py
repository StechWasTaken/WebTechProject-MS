import os
from project import app
from flask import Flask, render_template, Blueprint
from flask_sqlalchemy import SQLAlchemy
from project.models import *
from flask_login import current_user


# app.register_blueprint(bp_docent)
# https://flask.palletsprojects.com/en/1.1.x/blueprints/


@app.route('/')
def index():
    role = 'geen'
    if current_user.is_authenticated:
        role = getRole(current_user.id)

    return render_template('home.html', role = role, name = current_user.username)

if __name__ == "__main__":
    app.run(debug=True)

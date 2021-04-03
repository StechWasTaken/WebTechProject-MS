import os
from project import app
from flask import Flask, render_template, Blueprint
from flask_sqlalchemy import SQLAlchemy


# app.register_blueprint(bp_docent)
# https://flask.palletsprojects.com/en/1.1.x/blueprints/


@app.route('/')
def index():
    return render_template('home.html')

if __name__ == "__main__":
    app.run(debug=True)
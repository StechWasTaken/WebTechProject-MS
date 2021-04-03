import os
from project import app
from flask import Flask, render_template, Blueprint
from flask_sqlalchemy import SQLAlchemy
# from project.model import db

# app = Flask(__name__)

# app.register_blueprint(bp_docent)
# https://flask.palletsprojects.com/en/1.1.x/blueprints/

# db.init_app(app)

# Migrate(app, db)

@app.route('/')
def index():
    return render_template('home.html')

if __name__ == "__main__":
    app.run(debug=True)
from flask import Flask, render_template, Blueprint
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir + "/project/", 'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

@app.route('/')
def index():
    return render_template('home.html')

if __name__ == "__main__":
    app.run()
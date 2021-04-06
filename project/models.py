import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager
from flask_login import UserMixin


db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

class User(db.Model, UserMixin):

    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email       = db.Column(db.String(64), unique=True, index=True, nullable=False)
    username    = db.Column(db.String(64), unique=True, index=True, nullable=False)
    password    = db.Column(db.String(128), nullable=False)

    def __init__(self, username, email, password):
        self.username   = username
        self.email      = email
        self.password   = generate_password_hash(password)
        self.user_token = '123'

    def __repr__(self):
        return f"<User email={self.email} username={self.username}>"

    def check_password(self, password):
        return check_password_hash(self.password, password)
    

    roles = db.relationship("Role", secondary="user_roles")


class Role(db.Model):
    __tablename__   = 'roles'
    id              = db.Column(db.Integer, primary_key=True)
    name            = db.Column(db.String(16), unique=True, nullable=False)

    def __init__(self, role):
        self.name = name

    def __repr__(self):
        return f"<Role ={self.name}>"


class UserRoles(db.Model):
    __tablename__ = 'user_roles'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    role_id = db.Column(db.Integer, db.ForeignKey("roles.id"))


class Teacher(db.Model):

    __tablename__ = 'teachers'
    id          = db.Column(db.Integer, primary_key=True)
    email       = db.Column(db.String(64), unique=True, index=True, nullable=False)
    username    = db.Column(db.String(64), unique=True, index=True, nullable=False)
    password    = db.Column(db.String(128), nullable=False)

    def __init__(self, username, email, password):
        self.id         = id
        self.username   = username
        self.email      = email
        self.password   = generate_password_hash(password)

    def __repr__(self):
        return f"<Teacher id = {self.teacher_id}>"

class Language(db.Model):

    __tablename__ = 'languages'
    id          = db.Column(db.Integer, primary_key=True)
    language    = db.Column(db.Text, nullable=False)

    def __init__(self, language):
        self.language = language

    def __repr__(self):
        return f"<Language language={self.language}>"


class Lecture(db.Model):

    __tablename__ = 'lectures'
    id              = db.Column(db.Integer, primary_key=True)
    teacher_id      = db.Column(db.Integer, db.ForeignKey("teachers.id"))
    language_id     = db.Column(db.Integer, db.ForeignKey("languages.id"))
    start_time      = db.Column(db.Text, nullable=False) # format: d-m-y h:m
    location        = db.Column(db.Text, nullable=False)

    def __init__(self, start_time, location):
        self.start_time = start_time
        self.location = location

    def __repr__(self):
        return f"<Lecture start_time={self.start_time} location={self.location}>"


# association table: LECTURES <-> ATTENDANTS <-> USERS
lecture_attendants = db.Table(
    "lecture_attendants",
    db.Column("user_id", db.Integer, db.ForeignKey("users.id"), primary_key=True),
    db.Column("lecture_id", db.Integer, db.ForeignKey("lectures.id"), primary_key=True)
)

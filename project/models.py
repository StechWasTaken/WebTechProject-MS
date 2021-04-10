import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, UserMixin


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

    def __repr__(self):
        return f"<User email={self.email} username={self.username}>"

    def check_password(self, password):
        return check_password_hash(self.password, password)

    

class Role(db.Model):

    __tablename__   = 'roles'
    id              = db.Column(db.Integer, primary_key=True)
    name            = db.Column(db.String(16), unique=True, nullable=False)

    def __init__(self, name):
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


class Course(db.Model):

    __tablename__ = 'courses'
    id              = db.Column(db.Integer, primary_key=True)
    teacher_id      = db.Column(db.Integer, db.ForeignKey("teachers.id"))
    language_id     = db.Column(db.Integer, db.ForeignKey("languages.id"))
    location        = db.Column(db.Text, nullable=False)

    def __init__(self, start_time, location):
        self.start_time = start_time
        self.location = location

    def __repr__(self):
        return f"<Course start_time={self.start_time} location={self.location}>"

class Attendee(db.Model):
    
    __tablename__ = 'attendees'
    user_id     = db.Column(db.Integer, db.ForeignKey("users.id"), primary_key=True)
    course_id  = db.Column(db.Integer, db.ForeignKey("courses.id"), primary_key=True)

    def __init__(self, user_id, course_id):
        self.user_id = user_id
        self.course_id = course_id

    def __repr__(self):
        return f"<Attendee user_id={self.user_id} course_id={self.course_id}>"

class Lecture(db.Model):
    
    # date(day, month, year, hour, minute).strftime('%w %d %m %y %H %M')
    # deltatime = end_time - start_time
    # hours = ( deltatime.seconds - deltatime.seconds % 3600 ) // 3600
    # minutes = ( hours - hours % 60 ) // 60
    # seconds = ( minutes - minutes % 60 ) // 60

    __tablename__ = 'lectures'
    id                  = db.Column(db.Integer, primary_key=True)
    course_id           = db.Column(db.Integer, db.ForeignKey("courses.id"))
    start_time          = db.Column(db.DateTime) 
    end_time            = db.Column(db.DateTime)
    lecture_name        = db.Column(db.Text)






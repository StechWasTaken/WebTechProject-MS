from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):

    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email       = db.Column(db.Text, nullable=False)
    username    = db.Column(db.Text, nullable=False)
    password    = db.Column(db.Text, nullable=False)

    def __init__(self, username, email, password):
        self.username   = username
        self.email      = email
        self.password   = generate_password_hash(password)

    def __repr__(self):
        return f"<User email={self.email} username={self.username}>"

class Teacher(db.Model):

    __tablename__ = 'teachers'
    id = db.Column(db.Integer, primary_key=True)
    email       = db.Column(db.Text, nullable=False)
    username    = db.Column(db.Text, nullable=False)
    password    = db.Column(db.Text, nullable=False)

    def __init__(self, username, email, password):
        self.username   = username
        self.email      = email
        self.password   = generate_password_hash(password)

    def __repr__(self):
        return f"<Teacher email={self.email} username={self.username}>"

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
    start_time      = db.Column(db.DateTime, nullable=False)
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
    db.Column("lecture_id", db.Integer, db.ForeignKey("lectures.id"), primary_key=True),
)

db.create_all()
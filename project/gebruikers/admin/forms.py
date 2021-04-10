from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, IntegerField, SubmitField, DateTimeField
from wtforms.validators import DataRequired, Email, EqualTo
from wtforms import ValidationError
from project.models import *

class AddCourseForm(FlaskForm):
    """ teacher_id, language_id, location 
    teacher username, language name, location
    """

    username = StringField('Teacher Username', validators=[DataRequired()])
    language = StringField('Language', validators=[DataRequired()])
    location = StringField('Location', validators=[DataRequired()])
    submit = SubmitField('Add Course')

class AddLectureForm(FlaskForm):
    """ course_id', start_time, end_time, lecture_name)
    """
    course_name = StringField('Course Name', validators=[DataRequired()])
    start_time = DateTimeField('Start Time', validators=[DataRequired()])
    end_time = DateTimeField('End Time', validators=[DataRequired()])
    lecture_name = StringField('Lecture Name', validators=[DataRequired()])
    submit = SubmitField('Add Course')

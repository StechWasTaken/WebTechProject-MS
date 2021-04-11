from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, IntegerField, SubmitField, DateTimeField, TextAreaField, SelectField
from wtforms.validators import DataRequired, Email, EqualTo
from wtforms import ValidationError
from project.models import *



class AddCourseForm(FlaskForm):
    """ teacher_id, language_id, location 
    teacher username, language name, location
    """

    username = SelectField('Teacher Username', validators=[DataRequired()])
    language = SelectField('Language', validators=[DataRequired()])
    location = StringField('Location', validators=[DataRequired()])
    cost = StringField('Cost', validators=[DataRequired()])
    description = TextAreaField('Course Description', validators=[DataRequired()])    
    submit = SubmitField('Add Course')


# Dit is nu overbodig - verwijderen?
class AddLectureForm(FlaskForm):
    """ course_id', start_time, end_time, lecture_name)
    """
    course_id = StringField('Course Name', validators=[DataRequired()])
    start_time = DateTimeField('Start Time', validators=[DataRequired()])
    end_time = DateTimeField('End Time', validators=[DataRequired()])
    lecture_name = StringField('Lecture Name', validators=[DataRequired()])
    submit = SubmitField('Add Course')

    # def validate(self):
    #     if not Form.validate(self):
    #         return False
    #     course_id = form.course_id.data
    #     start_time = form.start_time.data
    #     end_time = form. end_time.data
    #     lecture_name = form.lecture_name.data

    #     if end_time <= start_time:
    #         return False

    #    return True

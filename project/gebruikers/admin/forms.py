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


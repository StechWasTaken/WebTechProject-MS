from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, IntegerField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo
from wtforms import ValidationError
from project.models import *

class AddRoleForm(FlaskForm):
    """uid & rolename """

    username = StringField('Username', validators=[DataRequired()])
    rolename = StringField('Role', validators=[DataRequired()])
    submit = SubmitField('Add Role')
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, IntegerField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo
from wtforms import ValidationError
from project.models import User

class AlterUsernameForm(FlaskForm):
    username = StringField('Gebruikersnaam', validators=[DataRequired()])
    submit = SubmitField('Wijzigen')

    def check_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('Deze gebruikersnaam is al vergeven, probeer een ander naam!')

class AlterEmailForm(FlaskForm):
    email = StringField('E-mail', validators=[DataRequired(), Email()])
    submit = SubmitField('Wijzigen')

    def check_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('Dit e-mailadres staat al geregistreerd!')

class AlterPasswordForm(FlaskForm):
    old_password = PasswordField('Oude wachtwoord', validators=[DataRequired()])
    new_password = PasswordField('Nieuwe wachtwoord', validators=[DataRequired(), EqualTo('pass_confirm',    message='Wachtwoord matched niet!')])
    new_pass_confirm = PasswordField('Bevestig nieuwe wachtwoord', validators=[DataRequired()])
    submit = SubmitField('Wijzigen')
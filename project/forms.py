from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, IntegerField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo
from wtforms import ValidationError
from project.models import User

class RegisterForm(FlaskForm):

    email = StringField('E-mail', validators=[DataRequired(), Email()])
    username = StringField('Gebruikersnaam', validators=[DataRequired()])
    password = PasswordField('Wachtwoord', validators=[DataRequired(), EqualTo('pass_confirm',    message='Wachtwoord matched niet!')])
    pass_confirm = PasswordField('Bevestig wachtwoord', validators=[DataRequired()])
    submit = SubmitField('Registreer')

    def check_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('Dit e-mailadres staat al geregistreerd!')

    def check_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('Deze gebruikersnaam is al vergeven, probeer een ander naam!')

class LoginForm(FlaskForm):
    email = StringField('E-mail', validators=[DataRequired(), Email()])
    password = PasswordField('Wachtwoord', validators=[DataRequired()])
    submit = SubmitField('Inloggen')


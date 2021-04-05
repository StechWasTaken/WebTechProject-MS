class VerwijderForm(FlaskForm):

    id = IntegerField('Vul het ID van de cursist in en klik op Verwijder:')
    submit = SubmitField('Verwijder')
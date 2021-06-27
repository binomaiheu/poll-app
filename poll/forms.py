from flask_wtf import FlaskForm
from flask_wtf.recaptcha import validators
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

class LoginForm(FlaskForm):
    secret_key = StringField('secret_key', validators=[DataRequired()])
    submit = SubmitField("Verzenden")

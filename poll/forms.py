from flask_wtf import FlaskForm
from flask_wtf.recaptcha import validators
from wtforms import StringField, SubmitField, IntegerField
from wtforms import FieldList, FormField
from wtforms.validators import DataRequired, InputRequired, NumberRange

class LoginForm(FlaskForm):
    secret_key = StringField('secret_key', validators=[DataRequired()])
    submit = SubmitField("Verzenden")


class QuestionForm(FlaskForm):
    """
    Form for an individual question with a rating
    """    
    rating = IntegerField('rating', validators=[InputRequired(), NumberRange(min=0, max=5)])


class PollForm(FlaskForm):
    """
    Form for a list of questions, see : https://newbedev.com/add-input-fields-dynamically-with-wtforms

    """
    questions = FieldList(FormField(QuestionForm), min_entries=1)
    submit = SubmitField("Verstuur")


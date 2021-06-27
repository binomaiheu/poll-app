from flask_wtf import FlaskForm

from wtforms import StringField, SubmitField
from wtforms.fields.html5 import IntegerRangeField
from wtforms import FieldList, FormField
from wtforms.validators import DataRequired, InputRequired, NumberRange

class LoginForm(FlaskForm):
    secret_key = StringField('secret_key', validators=[DataRequired()])
    submit = SubmitField("Verzenden")


class QuestionForm(FlaskForm):
    """
    Form for an individual question with a rating
    """    
    #rating = IntegerRangeField('rating', validators=[InputRequired(), NumberRange(min=0, max=5)])
    rating = IntegerRangeField('rating', render_kw={"min": 0, "max": 5, "step": 1 })


class PollForm(FlaskForm):
    """
    Form for a list of questions, see : https://newbedev.com/add-input-fields-dynamically-with-wtforms

    """
    questions = FieldList(FormField(QuestionForm), min_entries=1)
    submit = SubmitField("Verstuur")


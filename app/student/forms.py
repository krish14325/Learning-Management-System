from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    TextAreaField,
    SubmitField ,
    IntegerField
)
from wtforms.validators import (
    DataRequired,
    Length
)

class EnrollementForm(FlaskForm):
    submit = SubmitField("Enroll")
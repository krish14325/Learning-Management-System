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

class Course_create(FlaskForm):
    title = StringField("Title" , validators=[DataRequired()])
    description = TextAreaField("Description" , validators=[DataRequired()])
    submit = SubmitField("Create Course")

class lesson_create(FlaskForm):
    title = StringField("Title" , validators=[DataRequired()])
    content = TextAreaField("Content" , validators=[DataRequired()])
    position = IntegerField("Lesson Number" , validators=[DataRequired()])
    submit = SubmitField("Add Lesson")
    
class Deletelessonform(FlaskForm):
    submit = SubmitField("Delete Lesson")
from flask_wtf import FlaskForm
from wtforms import (
    StringField , 
    TextAreaField , 
    IntegerField , 
    SubmitField,
    SelectField,
    EmailField , 
    PasswordField
)
from wtforms.validators import (
    DataRequired , 
    Email , 
    Length , 
    EqualTo ,

)

class Registeration_form(FlaskForm):
    name = StringField("Username" , validators=[DataRequired() , Length(min=3 , max=100)])
    email = EmailField("Email" , validators=[DataRequired() , Email()])
    password = PasswordField("Password" , validators=[DataRequired() , Length(min=6 , max=100)])
    Confirm_password = PasswordField("Confirm Password" , validators=[DataRequired() , EqualTo("password" , message="Password Must Match.")])
    phone_number = StringField("Contact Number" , validators=[DataRequired() , Length(min=10 , max=15)])
    role = SelectField("Role" , choices=[
        ("Stu" , "Student"),
        ("Tea" , "Teacher")
    ] ,
        validators=[DataRequired()])
    submit = SubmitField("Register")
    
class Login_form(FlaskForm):
    email = EmailField("Email" , validators=[DataRequired() , Email()])
    password = PasswordField("Password" , validators=[DataRequired() , Length(min=6 , max=100)])
    submit = SubmitField("Login")
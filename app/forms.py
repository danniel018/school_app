from email.policy import default
from wtforms import StringField, SubmitField, PasswordField, \
    IntegerField, EmailField , SelectField, TextAreaField, DateField
from wtforms.validators import DataRequired, Length, InputRequired, EqualTo, AnyOf
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired

class Ids (FlaskForm):
    id=IntegerField("id",validators=[DataRequired()])

class Users(FlaskForm):
    email=EmailField("Email*",validators=[DataRequired(),Length(max=50,message="")])
    password = PasswordField("Password*",validators=[DataRequired()])


class New_user(Users):
    name=StringField("Name*",validators=[DataRequired(),Length(max=20,message="")]) 
    lastname=StringField("Lastname*",validators=[DataRequired(),Length(max=20,message="")]) 
    password2 = PasswordField('confirm password*',validators=[InputRequired(),EqualTo('password', message='Passwords are not equal')])
    add_user = SubmitField("Sign Up")    

class Login(Users):
    log_in = SubmitField("Log in")

class Events(FlaskForm):
    event_type = SelectField("Event type*", choices=[('Assignment'),('Exam'),
        ('Laboratory'),('Other')])
    name=StringField("Name*",validators=[DataRequired(),Length(max=50,message="")])
    description=TextAreaField("Description",validators=[Length(max=50,message="")])
    submit_date = DateField("Submit date*",validators=[DataRequired()])
    add_event = SubmitField("Add new")    

    
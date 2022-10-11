from email.policy import default
from wtforms import StringField, SubmitField, PasswordField, IntegerField, EmailField , RadioField
from wtforms.validators import DataRequired, Length, InputRequired, EqualTo, AnyOf
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired

class Ids (FlaskForm):
    id=IntegerField("id",validators=[DataRequired()])

class Users(FlaskForm):
    dni=IntegerField("DNI/c.c",validators=[DataRequired()])
    password = PasswordField("Password",validators=[DataRequired()])


class New_user(Users):
    name=StringField("Name",validators=[DataRequired(),Length(max=20,message="")])
    lastname=StringField("Lastname",validators=[DataRequired(),Length(max=20,message="")]) 
    email=EmailField("Email",validators=[DataRequired(),Length(max=50,message="")])
    cellphone=StringField("Cellphone",validators=[DataRequired(),Length(max=10,message="")])
    password2 = PasswordField('confirm password',validators=[InputRequired(),EqualTo('password', message='Passwords are not equal')])
    #child_dni = 
    access_code = PasswordField('Access code',validators=[InputRequired()])
    add_user = SubmitField("Sign Up")    

class Login(Users):
    log_in = SubmitField("Ingresar")
from wtforms import StringField, SubmitField, PasswordField, SelectField, IntegerField, \
    DateField,DecimalField, TextAreaField, BooleanField, RadioField, MultipleFileField, EmailField
from wtforms.validators import DataRequired, Length, InputRequired, EqualTo
from flask_wtf import FlaskForm 
from flask_wtf.file import FileField, FileRequired

class Ids (FlaskForm):
    id=IntegerField("id",validators=[DataRequired()])

class Users(FlaskForm):
    dni=StringField("DNI/c.c",validators=[DataRequired(),Length(max=15,message="usuario muy largo")])
    password = PasswordField("Password",validators=[DataRequired()])


class New_user(Users):
    name=StringField("Name",validators=[DataRequired(),Length(max=20,message="")])
    lastname=StringField("Lastname",validators=[DataRequired(),Length(max=20,message="")])
    email=EmailField("Email",validators=[DataRequired(),Length(max=50,message="")])
    cellphone=EmailField("Cellphone",validators=[DataRequired(),Length(max=10,message="")])
    password2 = PasswordField('confirm password',validators=[InputRequired(),EqualTo('password', message='Passwords are not equal')])
    profile_code = PasswordField('Access code',validators=[InputRequired()])
    add_user = SubmitField("Registrarse")

class Login(Users):
    log_in = SubmitField("Ingresar")
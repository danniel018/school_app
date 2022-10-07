from flask import Blueprint ,make_response, render_template,flash,redirect,url_for,request,jsonify
from flask_login import login_user, login_required, logout_user, current_user

from app.forms import New_user, Login 
from werkzeug.security import generate_password_hash,check_password_hash
from app.database import Database
from app.config import Access_code
from app.models import Userdata

auth = Blueprint('auth',__name__, url_prefix='/auth',template_folder='templates') 

@auth.route('/signup',methods=['GET','POST'])
def signup():
    
    if current_user.is_authenticated: 
        return redirect(url_for('warriors.inicio'))

    form = New_user()
    database = Database()
    code = Access_code()
    if form.add_user.data and form.validate():
        if form.access_code.data == code:
            hashed_password = generate_password_hash(form.password.data,'sha256')
            try:
                database.execute_query("INSERT INTO users (dni,password) VALUES (%s,%s)",
                    [form.dni.data,hashed_password])
                database.execute_query("INSERT INTO parents (name,lastname,email,cellphone,user_id)" 
                    "VALUES (%s,%s,%s,%s,LAST_INSERT_ID())",[form.name.data,form.lastname.data,form.email.data,form.cellphone.data])
                database.save()
                database.close()
                return redirect(url_for('auth.login'))

            except Exception as e:
                print(e)
                database.discard()
                return redirect(url_for('auth.signup'))    
        else:       
            flash("Wrong code!",category='danger')
            return redirect(url_for('auth.signup'))

    return render_template('auth/signup.html',form=form)

@auth.route('/login',methods=['GET','POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('warriors.warriors_home'))
    form = Login()
    database = Database("usuario")

    if form.log_in.data and form.validate():
        user = database.execute_query("SELECT usuario_id,nombre,apellido,usuario,contraseña,perfil FROM usuarios WHERE usuario = %s",1,[form.user.data])
        i = 0
        for user_data in user:
            if check_password_hash(user_data[4],form.password.data):
                logged_user = Userdata(user_data[0],user_data[1],user_data[2],user_data[3],user_data[5])
                login_user(logged_user)
                database.close()
                return redirect(url_for('warriors.warriors_home'))
            else:
                flash("Contraseña incorrecta",category='danger')
            i += 1
        if i == 0:
            flash("Usuario incorrecto",category='danger') 
    return render_template('auth/login.html',form=form)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect (url_for('auth.login'))
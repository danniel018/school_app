from flask import make_response, render_template,flash,redirect,url_for,request,jsonify
from flask_login import login_user, login_required, logout_user, current_user
from . import auth
from app.forms import New_user, Login 
from werkzeug.security import generate_password_hash,check_password_hash
from app.database import Database
from app.config import Profiles_codes
from app.models import Userdata

@auth.route('/registro',methods=['GET','POST'])
def signup():
    
    if current_user.is_authenticated: 
        return redirect(url_for('warriors.inicio'))

    form = New_user()
    conection = Database("Usuario","nombre de usuario")
    codes = Profiles_codes()
    if form.add_user.data and form.validate():
        codes_areas = vars(codes)
        x = 1
        for code in codes_areas.values():
            if code == form.profile_code.data and int(form.profile.data) == x:
                break
            else:
                x += 1
        print(x)
        if x != 6:
            hashed_password = generate_password_hash(form.password.data,'sha256')
            signup = conection.execute_query("INSERT INTO usuarios (nombre,apellido,usuario,contraseña,perfil) VALUES (%s,%s,%s,%s,%s)",3,[form.name.data,form.lastname.data,form.user.data,hashed_password,form.profile.data])
            if signup == 'ok':
                conection.close()
                return redirect(url_for('auth.login'))
            else:
                return redirect(url_for('auth.signup'))    
        else:       
            flash("Código de departamento incorrecto",category='danger')
            return redirect(url_for('auth.signup'))

    return render_template('auth/registro.html',form=form)

@auth.route('/login',methods=['GET','POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('warriors.warriors_home'))
    form = Login()
    conection = Database("usuario")

    if form.log_in.data and form.validate():
        user = conection.execute_query("SELECT usuario_id,nombre,apellido,usuario,contraseña,perfil FROM usuarios WHERE usuario = %s",1,[form.user.data])
        i = 0
        for user_data in user:
            if check_password_hash(user_data[4],form.password.data):
                logged_user = Userdata(user_data[0],user_data[1],user_data[2],user_data[3],user_data[5])
                login_user(logged_user)
                conection.close()
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
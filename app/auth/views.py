from flask import Blueprint ,make_response, render_template,flash,redirect,url_for,request,jsonify
from flask_login import login_user, login_required, logout_user, current_user

from app.forms import New_user, Login 
from werkzeug.security import generate_password_hash,check_password_hash
from app.database import Database
from app.config import Access_code
from app.models import Userdata
from app.database import db
auth = Blueprint('auth',__name__, url_prefix='/auth',template_folder='templates') 

@auth.route('/signup',methods=['GET','POST'])
def signup():
    
    if current_user.is_authenticated: 
        return redirect(url_for('parents.home'))

    form = New_user()
    database = Database()

    if form.add_user.data and form.validate():
        hashed_password = generate_password_hash(form.password.data,'sha256')
        try:
            database.modify_data("INSERT INTO users (name,lastname,email,password,user_type) VALUES (%s,%s,%s,%s,%s)",
                [form.name.data,form.lastname.data,form.email.data,hashed_password,'teacher'])
            database.save()
            database.close()
            flash("User signed up",category='success')
            return redirect(url_for('auth.login'))

        except Exception as e:
            print(e)
            database.discard()
            flash("error",category='danger')
            return redirect(url_for('auth.signup'))    
        

    return render_template('auth/signup.html',form=form)

@auth.route('/login',methods=['GET','POST'])
def login():
    # if current_user.is_authenticated:
    #     return redirect(url_for('warriors.warriors_home'))
    form = Login()
    #database = Database()

    if form.log_in.data and form.validate():
        #user = database.query_data("SELECT user_id,name,lastname,user_type,password FROM users WHERE email = %s",[form.email.data])
        user = db.session.execute("SELECT user_id,name,lastname,user_type,password FROM users WHERE email = :email",{'email':form.email.data})
        i = 0
        for user_data in user:
            if check_password_hash(user_data[4],form.password.data):
                logged_user = Userdata(user_data[0],user_data[1],user_data[2],user_data[3])
                login_user(logged_user)
                #database.close()
                if user_data[3] == 'teacher':
                    return redirect(url_for('teachers.home'))
                else:
                    return redirect(url_for('parents.home'))

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
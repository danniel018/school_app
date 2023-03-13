from flask import Blueprint,render_template,flash,redirect,url_for,current_app
from flask_login import login_user, login_required, logout_user, current_user

from app.forms import New_user, Login 
from werkzeug.security import generate_password_hash,check_password_hash

from app.models1 import Userdata
from app.database import db, QueriedData
auth = Blueprint('auth',__name__, url_prefix='/auth',template_folder='templates') 

# @auth.route('/signup',methods=['GET','POST']) 
# def signup():
    
#     if current_user.is_authenticated: 
#         return redirect(url_for('parents.home'))

#     form = New_user()
#     #database = Database()

#     if form.add_user.data and form.validate():
#         hashed_password = generate_password_hash(form.password.data,'sha256')
#         try:
#             bucket = current_app.config['TEACHERS_BUCKET']
#             db.session.execute("INSERT INTO users (name,lastname,email,password,user_type) "
#                         "VALUES (:nam, :last, :email, :pass, :ut)",
#                         {'nam':form.name.data,'last':form.lastname.data,'email':form.email.data,
#                                 'pass':hashed_password,'ut':'teacher'})
#             new_user = db.session.execute("SELECT LAST_INSERT_ID()")
#             new_user = QueriedData.return_one(new_user)
#             db.session.execute("UPDATE users SET bucket_name = :bucket WHERE "
#                                "user_id = :uid",{'bucket':f'{bucket}{str(new_user)}','uid':new_user})
#             db.session.commit()
#             flash("User signed up",category='success')
#             return redirect(url_for('auth.login'))

#         except Exception as e:
#             print(e)
#             db.session.rollback()
#             flash("error",category='danger')
#             return redirect(url_for('auth.signup'))    
        

#     return render_template('auth/signup.html',form=form)

@auth.route('/login',methods=['GET','POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('teachers.home'))
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
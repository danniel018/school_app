from flask import Blueprint ,make_response, render_template,flash,redirect,url_for,request,jsonify
from flask_login import login_user, login_required, logout_user, current_user

from app.forms import New_user, Login 
from werkzeug.security import generate_password_hash,check_password_hash
from app.database import Database
from app.config import Access_code


parents = Blueprint('parents',__name__, url_prefix='/parents',template_folder='templates') 

@parents.route('/home')
def home():
    

    return render_template('parents/home.html')
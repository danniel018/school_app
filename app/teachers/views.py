from flask import Blueprint ,make_response, render_template,flash,redirect,url_for,request,jsonify
from flask_login import login_user, login_required, logout_user, current_user

from app.forms import New_user, Login 
from werkzeug.security import generate_password_hash,check_password_hash
from app.database import Database
from app.config import Access_code
from app.models import Userdata

teachers = Blueprint('teachers',__name__, url_prefix='/teachers',template_folder='templates') 

@teachers.route('/home')
def home():
    

    return render_template('teachers/home.html')
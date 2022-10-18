from flask import Blueprint ,make_response, render_template,flash,redirect,url_for,request,jsonify
from flask_login import login_user, login_required, logout_user, current_user

from app.forms import New_user, Login 
from werkzeug.security import generate_password_hash,check_password_hash
from app.database import Database
from app.config import Access_code
from app.models import Userdata
from app.database import db

teachers = Blueprint('teachers',__name__, url_prefix='/teachers',template_folder='templates') 

@teachers.route('/home')
def home():
    

    return render_template('teachers/home.html')

@teachers.route('/classes')
def teacher_classes():
    
    classes = db.session.execute("SELECT gp.name,s.name FROM grade_groups as gp JOIN grades_subjects as gs "
        "ON gp.grade_group_id = gs.grade_group_id JOIN subjects as s ON s.subject_id = gs "
        ".subject_id WHERE gs.teacher_id = :id",{'id':current_user.id})

    lclass = [x for x in classes]

    return render_template('teachers/classes.html',classes=lclass)

@teachers.route('/classes/<string:group>')
def class_info(group):
    
    students = db.session.execute("SELECT c.name, c.lastname FROM children as c JOIN children_grade_groups a"
        "s cg ON c.child_id = cg.child_id JOIN grade_groups as gg ON cg.grade_group_id = "
        "gg.grade_group_id WHERE gg.name = :group ",{'group':group})


    return render_template('teachers/class_info.html',students = students) 
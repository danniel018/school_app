from flask import Flask
from flask_restful import Api
from flask_login import LoginManager
from .config import Config
from .models1 import Userdata 
from .auth import views
from .teachers.views import teachers
from .parents.views import parents
from .api.views import api
from .database import db
from .api.views import GroupGrades, Event, Grade, Teacherclasses, ClassChildren,\
    AnnouncementsResource, AnnouncementResource, ReportsResource, Classes
    


login_manager = LoginManager()
login_manager.login_message = ''
login_manager.login_view = 'auth.login'

@login_manager.user_loader
def load_user(id):
    return Userdata.get_user_info(id)

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)
    app.register_blueprint(views.auth)
    app.register_blueprint(teachers)
    app.register_blueprint(parents)
    
    login_manager.init_app(app)
    app_api = Api(api)
    app_api.add_resource(GroupGrades,'/grades/gradesubject/<int:subject_id>')
    app_api.add_resource(Event,'/events/<int:event_id>')
    app_api.add_resource(Grade,'/grades/<int:grade_id>')
    app_api.add_resource(Teacherclasses,'/teachers/groups/<int:teacher_id>')
    app_api.add_resource(ClassChildren,'/gradesubject/children/<int:subject_id>')
    app_api.add_resource(AnnouncementsResource,'/announcements')
    app_api.add_resource(AnnouncementResource,'/announcements/<int:teacher_id>')
    app_api.add_resource(ReportsResource,'/reports')
    app_api.add_resource(Classes,'/classes')

    
    app.register_blueprint(api) 



    return app
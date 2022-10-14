from flask import Flask
from flask_login import LoginManager
from .config import Config
from .models import Userdata
from .auth import views
from .teachers.views import teachers
from .parents.views import parents



login_manager = LoginManager()
login_manager.login_message = ''
login_manager.login_view = 'auth.login'

@login_manager.user_loader
def load_user(id):
    return Userdata.get_user_info(id)

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    app.register_blueprint(views.auth)
    app.register_blueprint(teachers)
    app.register_blueprint(parents)

    login_manager.init_app(app)

    return app
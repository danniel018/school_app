from flask import Flask
from flask_login import LoginManager
from .config import Config
from .models import Userdata
from .auth import views


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
    login_manager.init_app(app)

    return app
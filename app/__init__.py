from flask import Flask
from flask_login import LoginManager

from .models import Userdata



login_manager = LoginManager()
login_manager.login_message = ''
login_manager.login_view = 'auth.login'

@login_manager.user_loader
def load_user(id):
    return Userdata.get_user_info(id)

def create_app():
    app = Flask(__name__)
    
    login_manager.init_app(app)

    return app
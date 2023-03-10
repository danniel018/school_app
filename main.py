# from flask import Flask
# from flask_login import LoginManager
# from app.config import Config
# from app.models import Userdata
# from app.auth.views import auth


# login_manager = LoginManager()
# login_manager.login_message = ''
# login_manager.login_view = 'auth.login'

# @login_manager.user_loader
# def load_user(id):
#     return Userdata.get_user_info(id)

# def create_app():
#     app = Flask(__name__, template_folder='templates')
#     app.config.from_object(Config)
#     app.register_blueprint(auth) 
#     login_manager.init_app(app)

#     return app

# if __name__ == "__main__":
#     app = create_app() 
#     app.run(debug=True)

from app import create_app   
app = create_app()  

if __name__ == "__main__": 
    app.run()
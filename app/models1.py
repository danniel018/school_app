from flask_login import UserMixin
from .database import Database 

class Userdata(UserMixin):
    def __init__(self,id,name,lastname,user_type):
        self.id = id
        self.name = name
        self.lastname = lastname 
        self.user_type = user_type
        

    @staticmethod
    def get_user_info(id):
        conection = Database()
        user_info = conection.query_data("SELECT user_id,name,lastname,user_type FROM users WHERE user_id = %s",[id])
        for user in user_info:
            return Userdata(user[0], user[1], user[2], user[3])
            
	
from flask_login import UserMixin
from .database import db 

class Userdata(UserMixin):
    def __init__(self,id,name,lastname,user_type):
        self.id = id
        self.name = name
        self.lastname = lastname 
        self.user_type = user_type
        

    @staticmethod
    def get_user_info(id):
        
        user_info = db.session.execute("SELECT user_id,name,lastname,user_type "
                            "FROM users WHERE user_id = :uid",{'uid':id})
        for user in user_info:
            return Userdata(user[0], user[1], user[2], user[3])
            
	
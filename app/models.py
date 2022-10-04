from flask_login import UserMixin
from .database import Database 

class Userdata(UserMixin):
    def __init__(self,id,nombre,apellido,usuario,perfil):
        self.id = id
        self.nombre = nombre
        self.apellido = apellido
        self.usuario = usuario
        self.perfil = perfil
        

    @staticmethod
    def get_user_info(id):
        conection = Database()
        user_info = conection.execute_query("SELECT usuario_id,nombre,apellido,usuario,perfil FROM usuarios WHERE usuario_id = %s",1,[id])
        for user in user_info:
            return Userdata(user[0], user[1], user[2], user[3],user[4])
            
	
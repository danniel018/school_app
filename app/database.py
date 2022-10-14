import mysql.connector
from flask import flash
from .config import DB_connection
import os
import logging

cloud_user = os.environ.get('CLOUD_SQL_USERNAME')
cloud_db_password = os.environ.get('CLOUD_SQL_PASSWORD')
cloud_db_name = os.environ.get('CLOUD_SQL_DATABASE_NAME')
cloud_connection_name = os.environ.get('CLOUD_SQL_CONNECTION_NAME')



class Database:
    
    def __init__(self):
        
        if os.environ.get('GAE_ENV') == 'standard':
            unix_socket = '/cloudsql/{}'.format(cloud_connection_name)

            self.db = mysql.connector.connect(user=cloud_user, password=cloud_db_password,
                                    unix_socket=unix_socket, db=cloud_db_name)
        else:
            self.db = mysql.connector.connect(host=DB_connection.host,user=DB_connection.user,
                password=DB_connection.password,database=DB_connection.database)
  
        self.cursor = self.db.cursor(buffered =True)
        
    def query_data(self,query):
        self.cursor.execute(query)
        
    def modify_data(self,query,data):
        self.cursor.execute(query,data)
        
        


    def save(self):
        self.db.commit()
        
    def discard(self):
        self.db.rollback()
    
    def close(self):
        self.cursor.close()
        self.db.close()
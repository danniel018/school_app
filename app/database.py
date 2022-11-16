import mysql.connector
from flask import flash
from .config import DB_connection
import os
import logging
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

cloud_user = os.environ.get('CLOUD_SQL_USERNAME')
cloud_db_password = os.environ.get('CLOUD_SQL_PASSWORD')
cloud_db_name = os.environ.get('CLOUD_SQL_DATABASE_NAME')
cloud_connection_name = os.environ.get('CLOUD_SQL_CONNECTION_NAME')


class QueriedData:

    @classmethod
    def return_one(cls,cursor):

        data = [x[0] for x in cursor]
        return data[0]


    @classmethod
    def return_row(cls,cursor):

        data = [x for x in cursor]
          
        return data[0] 

    @classmethod
    def return_rows(cls,cursor):
        print(cursor)
        print('sdfsd')
        return [x for x in cursor]  

    
    @classmethod
    def return_dic(cls,cursor,*keys):
        
        main = []
        for x in cursor:
            data = {}
            for y in range(len(keys)):
                data[keys[y]] = x[y]
            main.append(data)

        return main


                

              
        


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
        
    def query_data(self,query,data,return_data=0):
        self.cursor.execute(query,data)
        if return_data == 0:
            return self.cursor
        
    def modify_data(self, query:str, data:list):
        self.cursor.execute(query,data)
        
    def save(self):
        self.db.commit()
        
    def discard(self):
        self.db.rollback()
    
    def close(self):
        self.cursor.close()
        self.db.close()
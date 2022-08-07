from flask import *
import mysql.connector
from connection import pool

class UserModel:
    def connection(self):
        try:
            connection = pool.get_connection()
            return connection
        except:
            return 'error'

    def register(self, name, email, password):
        try:
            connection = self.connection()
            cursor = connection.cursor()
            cursor.execute('INSERT INTO `user` (`name`,`email`,`password`) VALUES (%s,%s,%s);',
            (name, email, password))
            user = cursor.fetchone()
            return user
        except:
            connection.rollback()
            return 'error'
        finally:
            cursor.close()
            connection.commit()
            connection.close()

    def login(self, email):
        try:
            connection = self.connection()
            cursor = connection.cursor()
            cursor.execute('SELECT * FROM `user` WHERE `email`= %s ;',(email,))
            user = cursor.fetchone()
            return user
        except:
            connection.rollback()
            return 'error'
        finally:
            cursor.close()
            connection.close()

user_model = UserModel()
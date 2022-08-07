from flask import *
import mysql.connector
from connection import pool

class UrlModel:
    def connection(self):
        try:
            connection = pool.get_connection()
            return connection
        except:
            return 'error'

    def select(self, short_url):
        try:
            connection = self.connection()
            cursor = connection.cursor()
            cursor.execute('SELECT * FROM `user` WHERE `short_url`= %s ;',(short_url,))
            url = cursor.fetchone()
            return url
        except:
            connection.rollback()
            return 'error'
        finally:
            cursor.close()
            connection.close()
    
    def check_count(self, short_url):
        try:
            connection = self.connection()
            cursor = connection.cursor()
            cursor.execute('SELECT COUNT(*) FROM `user` WHERE `short_url` = %s;',(short_url,))
            url = cursor.fetchone()
            return url
        except:
            connection.rollback()
            return 'error'
        finally:
            cursor.close()
            connection.close()

    def generate(self, id, long_url, short_url):
        try:
            connection = self.connection()
            cursor = connection.cursor()
            cursor.execute('UPDATE `user` SET `long_url` = %s,`short_url` = %s WHERE `id`= %s ;'
            ,(long_url, short_url, id))
            url = cursor.fetchone()
            return url
        except:
            connection.rollback()
            return 'error'
        finally:
            cursor.close()
            connection.commit()
            connection.close()

    def modify(self, id, short_url):
        try:
            connection = self.connection()
            cursor = connection.cursor()
            cursor.execute('UPDATE `user` SET `short_url` = %s WHERE `id`= %s ;',(short_url, id))
            url = cursor.fetchone()
            return url
        except:
            connection.rollback()
            return 'error'
        finally:
            cursor.close()
            connection.commit()
            connection.close()

    def delete(self, id):
        try:
            connection = self.connection()
            cursor = connection.cursor()
            cursor.execute('UPDATE `user` SET `short_url` = %s WHERE `id`= %s ;',('', id))
            url = cursor.fetchone()
            return url
        except:
            connection.rollback()
            return 'error'
        finally:
            cursor.close()
            connection.commit()
            connection.close()

url_model = UrlModel()
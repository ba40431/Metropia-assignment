import mysql.connector
from mysql.connector import Error,pooling
import os
from dotenv import load_dotenv

load_dotenv('.env')

pool = pooling.MySQLConnectionPool(
    pool_name ='MySQLPool',
    pool_size = 5,
	pool_reset_session = True,
    host = os.getenv('host'),
    user = os.getenv('user'),
    password = os.getenv('password'),
    database = os.getenv('database'),
)
try:
    connection = pool.get_connection()
except:
    print("連線資料庫失敗！")
finally:
    connection.close()


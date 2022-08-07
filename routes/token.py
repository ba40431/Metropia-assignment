from flask import *
import jwt
import time
import os
from dotenv import load_dotenv

load_dotenv(".env")

class UseJWT:
    def make_token(self, id, name, email):
        key = os.getenv('jwt_key')
        now = time.time()
        expiretime = 60*60
        payload = {
            'id': id,
            'name': name,
            'email': email,
            'exp': now + expiretime
        }
        token = jwt.encode(payload, key, algorithm = 'HS256')
        return token

    def get_token(self):
        jwt = request.cookies.get('token')
        return jwt

    def set_token(self,id, name, email, data):
        token = self.make_token(id, name, email)
        response = make_response(data)
        response.set_cookie(key = 'token', value = token, expires = time.time() + 60*60, httponly = True)
        return response

    def delete_token(self,data):
        response = make_response(data)
        response.set_cookie(key = 'token', value = '', expires = 0)
        return response

use_jwt = UseJWT()
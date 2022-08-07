from flask import *
from model.user import user_model
import json
import re
from flask_bcrypt import bcrypt
import jwt
from routes.token import use_jwt
import os
from dotenv import load_dotenv

load_dotenv('.env')

get_user = Blueprint('get_user', __name__, static_folder = 'static', template_folder = 'templates')
post_user = Blueprint('post_user', __name__, static_folder = 'static', template_folder = 'templates')
patch_user = Blueprint('patch_user', __name__, static_folder = 'static', template_folder = 'templates')
delete_user = Blueprint('delete_user', __name__, static_folder = 'static', template_folder = 'templates')

@get_user.route('/api/user', methods = ['GET'])
def get():
    token = use_jwt.get_token()
    if token:
        try:
            jwt_key = os.getenv('jwt_key')
            decode_token = jwt.decode(token, jwt_key, algorithms = ['HS256'])
            user = user_model.login(decode_token['email'])
            if user:
                data = {
                    'data': {
                        'id': user[0],
                        'name': user[1],
                        'email': user[2],
                        'pathName': user[5]
                    }
                }
                response = make_response(jsonify(data))
            else:
                data = {
                    'data':None
                }
                response = make_response(jsonify(data))
        except:
            data = {
                'data':None
            }
            response = use_jwt.delete_token(jsonify(data))
    else:
        data = {
            'data':None
        }
        response = make_response(jsonify(data))
    return response

@post_user.route('/api/user', methods = ['POST'])
def post():
    user_data = request.get_json()
    email_pattern = '^([\w\.\-]){1,64}\@([\w\.\-]){1,64}$' #正則表達式
    password_pattern = '^[0-9a-zA-Z_]+$'
    if re.match(email_pattern, user_data['email']) and re.match(password_pattern, user_data['password']):
        user = user_model.login(user_data['email'])
        if user:
            if user_data['name'] == '' or user_data['password'] == '':
                data = {
                    'error': True,
                    'message': '請輸入姓名、電子郵件和密碼'
                }
                response = make_response(jsonify(data), 400)
            else:
                data = {
                    'error': True,
                    'message': '註冊失敗，此電子信箱已被註冊'
                }
                response = make_response(jsonify(data), 400)
        elif user == 'error':
            data = {
                'error': True,
                'message': '伺服器內部錯誤'
            }
            response = make_response(jsonify(data), 500)
        elif user == None:
            if user_data['name'] == '' or user_data['email'] == '' or user_data['password'] ==  '':
                data = {
                    'error': True,
                    'message': '請輸入姓名、電子郵件和密碼'
                }
                response = make_response(jsonify(data), 400)
            else:
                hash_password = bcrypt.hashpw(user_data['password'].encode('utf-8'),bcrypt.gensalt()) #雜湊密碼
                register = user_model.register(user_data['name'],user_data['email'],hash_password)
                data = {'ok': True}
                response = make_response(jsonify(data))
    elif user_data['name'] == '' or user_data['email'] == '' or user_data['password'] == '':
        data = {
            'error': True,
            'message': '請輸入姓名、電子郵件和密碼'
        }
        response = make_response(jsonify(data), 400)
    elif re.match(email_pattern, user_data['email']) == None:
        data = {
            'error': True,
            'message': "電子信箱格式須包含「@」"
        }
        response = make_response(jsonify(data), 400)
    else:
        data = {
            'error': True,
            'message': '請勿在密碼輸入特殊符號'
        }
        response = make_response(jsonify(data),400)
    return response

@patch_user.route('/api/user', methods = ['PATCH'])
def patch():
    user_data = request.get_json()
    user = user_model.login(user_data['email'])
    if user:
        if  user_data['email'] == user[2] and bcrypt.checkpw(user_data['password'].encode('utf-8'), user[3].encode('utf-8')):
            data = {
                'ok': True,
                'userId': user[0]
            }
            response = use_jwt.set_token(user[0], user[1], user[2], jsonify(data))
        elif user_data['password'] == '':
            data = {
                'error': True,
                'message': '請輸入電子信箱和密碼'
            }
            response = make_response(jsonify(data), 400)
        else:
            data = {
                'error': True,
                'message': '登入失敗，電子信箱或密碼輸入錯誤'
            }
            response = make_response(jsonify(data), 400)
    elif user == 'error':
        data = {
            'error': True,
            'message': '伺服器內部錯誤'
        }
        response = make_response(jsonify(data), 500)
    elif user == None:
        if user_data['email'] == '' or user_data['password'] == '':
            data = {
                'error': True,
                'message': '請輸入電子信箱和密碼'
            }
            response = make_response(jsonify(data), 400)
        else:
            data = {
                'error': True,
                'message': '登入失敗，電子信箱或密碼輸入錯誤'
            }
            response = make_response(jsonify(data), 400)
    return response


@delete_user.route('/api/user', methods = ['DELETE'])
def delete():
    data = {'ok': True}
    response = use_jwt.delete_token(jsonify(data))
    return response
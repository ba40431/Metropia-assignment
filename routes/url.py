from flask import *
from model.url import url_model
import json
from flask_bcrypt import bcrypt
import jwt
from routes.token import use_jwt
import os
from dotenv import load_dotenv

load_dotenv('.env')

get_url = Blueprint('get_url', __name__, static_folder = 'static', template_folder = 'templates')
post_url = Blueprint('post_url', __name__, static_folder = 'static', template_folder = 'templates')
patch_url = Blueprint('patch_url', __name__, static_folder = 'static', template_folder = 'templates')
delete_url = Blueprint('delete_url', __name__, static_folder = 'static', template_folder = 'templates')

@get_url.route('/short-url/<pathName>', methods = ['GET'])
def get(pathName):
    user_url = url_model.select(pathName)
    return redirect(user_url[4])

@post_url.route('/api/url', methods = ['POST'])
def post():
    token = use_jwt.get_token()
    if token:
            jwt_key = os.getenv('jwt_key')
            decode_token = jwt.decode(token, jwt_key, algorithms = ['HS256'])
            if decode_token:
                url_data = request.get_json()
                long_url = url_data['longUrl']
                user_id = url_data['userId']
                pathName =  str(user_id)
                insert_DB = url_model.generate(user_id, long_url, pathName)
                if insert_DB == 'error':
                    data = {
                        'error': True,
                        'message': '伺服器內部錯誤'
                    }
                    response = make_response(jsonify(data), 500)
                else:
                    data = {
                        'ok': True,
                        'pathName': pathName
                    }
                    response = make_response(jsonify(data))
            else:
                data = {
                    'error': True,
                    'message': '未登入系統，拒絕存取'
                }
                response = make_response(jsonify(data), 403)
    else:
        data = {
            'error': True,
            'message': '未登入系統，拒絕存取'
        }
        response = make_response(jsonify(data), 403)
    return response

@patch_url.route('/api/url', methods = ['PATCH'])
def patch():
    token = use_jwt.get_token()
    if token:
            jwt_key = os.getenv('jwt_key')
            decode_token = jwt.decode(token, jwt_key, algorithms = ['HS256'])
            if decode_token:
                url_data = request.get_json()
                user_id = url_data['userId']
                new_path_name = url_data['newPathName']
                check_DB = url_model.check_count(new_path_name)
                if check_DB == (0,):
                    update_DB = url_model.modify(user_id, new_path_name)
                    if update_DB == 'error':
                        data = {
                            'error': True,
                            'message': '伺服器內部錯誤'
                        }
                        response = make_response(jsonify(data), 500) 
                    else:
                        data = {'ok': True}
                        response = make_response(jsonify(data), 200) 
                elif check_DB == 'error':
                    data = {
                        'error': True,
                        'message': '伺服器內部錯誤'
                    }
                    response = make_response(jsonify(data), 500)
                else:
                    data = {
                        'error': True,
                        'message': '此短網址名稱已存在'
                    }
                    response = make_response(jsonify(data), 400)
            else:
                data = {
                    'error': True,
                    'message': '未登入系統，拒絕存取'
                }
                response = make_response(jsonify(data), 403)
    else:
        data = {
            'error': True,
            'message': '未登入系統，拒絕存取'
        }
        response = make_response(jsonify(data), 403)
    return response

@delete_url.route('/api/url', methods = ['DELETE'])
def delete():
    token = use_jwt.get_token()
    if token:
            jwt_key = os.getenv('jwt_key')
            decode_token = jwt.decode(token, jwt_key, algorithms = ['HS256'])
            if decode_token:
                url_data = request.get_json()
                user_id = url_data['userId']
                update_DB = url_model.delete(user_id)
                if update_DB == 'error':
                    data = {
                        'error': True,
                        'message': '伺服器內部錯誤'
                    }
                    response = make_response(jsonify(data), 500)
                else:
                    data = {'ok': True}
                    response = make_response(jsonify(data))
            else:
                data = {
                    'error': True,
                    'message': '未登入系統，拒絕存取'
                }
                response = make_response(jsonify(data), 403)
    else:
        data = {
            'error': True,
            'message': '未登入系統，拒絕存取'
        }
        response = make_response(jsonify(data), 403)
    return response
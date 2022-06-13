import json
from flask import Flask, request, jsonify, make_response, g, redirect
import sqlite3
import time
import jwt, datetime, time
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

SECRET_KEY = "bearer token"
db = sqlite3.connect('server.db', check_same_thread=False)
sql = db.cursor()

app = Flask(__name__)
limiter = Limiter(
    app,
    key_func=get_remote_address,
)

users = dict()


@app.route('/', methods=['POST'])
@limiter.limit("3/minute")
def authorize_user():
    token = request.headers.get('Authorization').split()[1]
    success = verify_token(token)
    users[request.remote_addr] = success
    if success:
        data = {'message': 'Done', 'code': 'SUCCESS'}
        return make_response(jsonify(data), 200)
    else:
        return make_response(
            jsonify(
                {"message": "Пожалуйста, передайте правильную информацию заголовка подтверждения"}
            ),
            401,
        )


@app.route('/test', methods=['GET'])
def auth_test():
    message = {'message': 'Authorized', 'code': 'SUCCESS'} if users.get(request.remote_addr) else {
        "message": "Пожалуйста, передайте правильную информацию заголовка подтверждения"}
    response_code = 200 if users.get(request.remote_addr) else 401
    return make_response(jsonify(message), response_code)


def verify_token(token):
    token = decode_auth_token(auth_token=token)
    if token == 'Invalid Token ' or token == 'Token expired ':
        return False
    user_id = token['data']['id']
    sql.execute(f"SELECT id FROM users WHERE id = '{user_id}'")
    id_user = sql.fetchone()

    if id_user is None:
        return False

    return True


def decode_auth_token(auth_token):
    try:
        payload = jwt.decode(auth_token, SECRET_KEY, algorithms=['HS256'], options={'verify_exp': False})
        if 'data' in payload and 'id' in payload['data']:
            return payload
        else:
            raise jwt.InvalidTokenError
    except jwt.ExpiredSignatureError:
        return 'Token expired '
    except jwt.InvalidTokenError:
        return 'Invalid Token '


app.run(debug=True)

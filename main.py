import json
from flask import Flask, request, jsonify, make_response
import sqlite3

db = sqlite3.connect('server.db', check_same_thread=False)
sql = db.cursor()

app = Flask(__name__)

# sql.execute("SELECT token FROM users")
# print(sql.fetchall())

@app.route('/', methods=['POST'])
def authorize_user():
    data = json.loads(request.data)
    print(request.remote_addr)
    success = verify_token(request.headers.get('Authorization'))
    if success:
        data = {'message': 'Done', 'code': 'SUCCESS'}
        return make_response(jsonify(data), 200)
    else:
        return make_response(
            jsonify(
                {"message": "Неверный логин или пароль"}
            ),
            401,
        )


def verify_token(token):
    token = token.split(" ")[1]
    sql.execute(f"SELECT token FROM users WHERE token = '{token}'")
    token_db = sql.fetchone()
    if token_db:
        token_db = token_db[0]
    else:
        token_db = False
    if token == token_db:
        return True
    return False


app.run(debug=True)

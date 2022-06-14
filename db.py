import jwt, datetime, time
from flask import jsonify, g
import sqlite3

SECRET_KEY = "bearer token"
db = sqlite3.connect('server.db')
sql = db.cursor()


def table_creation_db():
    sql.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
            login TEXT,
            password TEXT,
            token TEXT,
            ip TEXT
        );
    """)
    db.commit()


def encode_auth_token(user, user_id):
    try:
        payload = {
            'exp': datetime.datetime.utcnow() + datetime.timedelta(days=2, seconds=10),
            'iat': datetime.datetime.utcnow(),
            'iss': user,
            'data': {
                'id': user_id,
            }
        }
        return jwt.encode(
            payload,
            SECRET_KEY,
            algorithm='HS256'
        )
    except Exception as e:
        return e


def user_creation(user, user_id, password, ip):
    token = encode_auth_token(user=user, user_id=user_id)
    sql.execute("INSERT INTO users VALUES (?, ?, ?, ?, ?)", (user_id, user, password, token, ip))
    db.commit()


def show_table_users():
    sqlite_select_query = """SELECT * from users"""
    cursor = db.cursor()
    cursor.execute(sqlite_select_query)
    records = cursor.fetchall()
    print(records)

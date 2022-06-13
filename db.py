import jwt, datetime, time
from flask import jsonify, g
import sqlite3


SECRET_KEY = "bearer token"
db = sqlite3.connect('server.db')
sql = db.cursor()


def encode_auth_token():
    try:
        payload = {
            'exp': datetime.datetime.utcnow() + datetime.timedelta(days=2, seconds=10),
            'iat': datetime.datetime.utcnow(),
            'iss': 'User_2',
            'data': {
                'id': 3,
            }
        }
        return jwt.encode(
            payload,
            SECRET_KEY,
            algorithm='HS256'
        )
    except Exception as e:
        return e


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

sql.execute("INSERT INTO users VALUES (?, ?, ?, ?, ?)", (3, 'User_2', 'qwe_2', encode_auth_token(), '127.0.0.3'))
db.commit()

sqlite_select_query = """SELECT * from users"""
cursor = db.cursor()
cursor.execute(sqlite_select_query)
records = cursor.fetchall()
print(records)

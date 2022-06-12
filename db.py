import sqlite3

db = sqlite3.connect('server.db')
sql = db.cursor()

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

sql.execute("INSERT INTO users VALUES (?, ?, ?, ?, ?)", (1, 'User', 'qwe', 'QwE1', '127.0.0.1'))
db.commit()

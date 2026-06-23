import sqlite3
from werkzeug.security import generate_password_hash

def get_db():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db()
    conn.execute('''
        CREATE TABLE IF NOT EXISTS visitors (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            visitor_name TEXT NOT NULL,
            student_name TEXT NOT NULL,
            room_number TEXT NOT NULL,
            purpose TEXT NOT NULL,
            in_time TEXT NOT NULL,
            out_time TEXT NOT NULL DEFAULT 'Still Inside',
            status TEXT DEFAULT 'Inside'
        )
    ''')
    conn.commit()
    conn.close()
    conn.execute('''
                 CREATE TABLE IF NOT EXISTS users (
                 
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT NOT NULL UNIQUE,
                    password TEXT NOT NULL
                 )
                    ''')
    conn.commit()
    conn.close()

if __name__ == '__main__':
    init_db()
    print("New database creates with in_time column ✅")
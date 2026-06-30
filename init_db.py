import os
import sqlite3
from werkzeug.security import generate_password_hash

def init_db():
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    DB_PATH = os.path.join(BASE_DIR,'database.db')
    
    conn = sqlite3.connect('DB_PATH')
    cursor = conn.cursor()
    
    # Visitors table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS visitors (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            visitor_name TEXT NOT NULL,
            student_name TEXT NOT NULL,
            type TEXT NOT NULL,
            purpose TEXT NOT NULL,
            in_time TEXT NOT NULL,
            out_time TEXT,
            status TEXT DEFAULT 'Inside'
        )
    ''')
    
    # Users table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            role TEXT DEFAULT 'visitor'
        )
    ''')
    
    # Default admin user
    hashed_password = generate_password_hash('admin123')
    cursor.execute("INSERT OR IGNORE INTO users (username, password, role) VALUES (?, ?, ?)",
                   ('admin', hashed_password, 'admin'))
    
    conn.commit()
    conn.close()
    print("Database ready! Tables created.")

if __name__ == '__main__':
    init_db()
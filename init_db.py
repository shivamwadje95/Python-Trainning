import sqlite3
from werkzeug.security import generate_password_hash

conn = sqlite3.connect('database.db')
cursor = conn.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS visitors (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    visitor_name TEXT NOT NULL,
    student_name TEXT NOT NULL,
    room_number TEXT NOT NULL,
    purpose TEXT NOT NULL,
    in_time TEXT NOT NULL,
    out_time TEXT,
    status TEXT DEFAULT 'Inside'
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL
)
''')

try:
    cursor.execute("ALTER TABLE users ADD COLUMN role TEXT DEFAULT 'visitor'")
except sqlite3.OperationalError:
    pass

hashed_password = generate_password_hash('admin123')
cursor.execute("INSERT OR IGNORE INTO users (username, password, role) VALUES (?, ?, ?)", 
               ('admin', hashed_password, 'admin'))

conn.commit()
conn.close()
print("Database ready! Tables created.")
print("Login: admin / admin123")
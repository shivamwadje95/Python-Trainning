import sqlite3
from werkzeug.security import generate_password_hash

conn = sqlite3.connect('database.db')
cursor = conn.cursor()

# Visitors table
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

# Users table for login
cursor.execute('''
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL
)
''')

# Default admin user - hashed password ke saath
hashed_password = generate_password_hash('admin123')
cursor.execute("DELETE FROM users")  # Purane users hata de
cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", ('admin', hashed_password))

conn.commit()
conn.close()
print("Database ready! Tables created.")
print("Login: admin / admin123")
import sqlite3
from flask import Flask, render_template, request

app = Flask(__name__)
app.secret_key = 'python2026'

def get_db():
    conn = sqlite3.connect('hostel.db')
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db()
    conn.execute('''CREATE TABLE IF NOT EXISTS visitors(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        visiting TEXT NOT NULL,
        room TEXT NOT NULL,
        purpose TEXT NOT NULL,
        in_time TEXT NOT NULL,
        out_time TEXT DEFAULT 'Still Inside',
        status TEXT DEFAULT 'Inside'
    )''')
    conn.execute("INSERT OR IGNORE INTO visitors (visiting, room, purpose, in_time) VALUES ('Kalash Pawar', '101', 'Friend', '10-06-2026 01:57')")
    conn.execute("INSERT OR IGNORE INTO visitors (visiting, room, purpose, in_time) VALUES ('Hariom Pawar', '102', 'Delivery', '10-06-2026 01:59')")
    conn.execute("INSERT OR IGNORE INTO visitors (visiting, room, purpose, in_time) VALUES ('Siya Sharma', '201', 'Guest', '13-06-2026 03:21')")
    conn.execute("INSERT OR IGNORE INTO visitors (visiting, room, purpose, in_time) VALUES ('Ritu Patil', '301', 'Family', '13-06-2026 03:26')")
    conn.commit()
    conn.close()


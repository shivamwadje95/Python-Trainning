from flask import Flask, render_template, request, redirect, url_for, flash
from datetime import datetime
import sqlite3

app = Flask(__name__)
app.secret_key = 'hostel-visitor-secret-key'

def get_db():
    conn = sqlite3.connect('hostel.db')
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db()
    conn.execute('''
        CREATE TABLE IF NOT EXISTS
        visitors (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            visitor_name TEXT NOT NULL,
            student_name TEXT NOT NULL,
            room_number TEXT NOT NULL,
            purpose TEXT NOT NULL,
            check_in TEXT NOT NULL,
            status TEXT DEFAULT 'Inside'
        )
    ''')
    conn.commit()
    conn.close()

init_db()

@app.route('/')
def home():
    conn = get_db()
    today = datetime.now().strftime("%Y-%m-%d")
    total = conn.execute("SELECT COUNT(*) FROM visitors WHERE check_in LIKE?", (today+'%',)).fetchone()[0]
    inside = conn.execute("SELECT COUNT(*) FROM visitors WHERE status = 'Inside'").fetchone()[0]
    conn.close()
    return render_template('home.html', total=total, inside=inside)

@app.route('/records')
def records():
    conn = get_db()
    visitors = conn.execute('SELECT * FROM visitors ORDER BY id ASC').fetchall()
    conn.close()
    return render_template('records.html', visitors=visitors)

@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        visitor_name = request.form['visitor_name']
        student_name = request.form['student_name']
        room_number = request.form['room_number']
        purpose = request.form['purpose']
        
        if not visitor_name or not student_name or not room_number or not purpose:
            flash('All fields are required!', 'danger')
            return render_template('add.html')
        
        conn = get_db()
        conn.execute(
            'INSERT INTO visitors (visitor_name, student_name, room_number, purpose, check_in) VALUES (?,?,?,?,?)',
            (visitor_name, student_name, room_number, purpose, datetime.now().strftime("%Y-%m-%d %H:%M"))
        )
        conn.commit()
        conn.close()
        
        flash('Visitor added successfully!', 'success')
        return redirect(url_for('records'))
    
    return render_template('add.html')

@app.route('/about')
def about():
    return render_template('about.html')

if __name__ == '__main__':
    app.run(debug=True)
import sqlite3
from flask import Flask, render_template, request, redirect

app = Flask(__name__)

# 1. get_db() function
def get_db():
    conn = sqlite3.connect('practice.db')  # hostel.db se alag
    conn.row_factory = sqlite3.Row
    return conn

# 2. init_db() apna table
def init_db():
    conn = get_db()
    conn.execute('''
        CREATE TABLE IF NOT EXISTS practice (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            task TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

# 3. One SELECT route - Home page pe saare tasks dikhao
@app.route('/')
def home():
    conn = get_db()
    tasks = conn.execute('SELECT * FROM practice ORDER BY id DESC').fetchall()
    conn.close()
    return render_template('prhome.html', tasks=tasks)

# 4. One INSERT route - Naya task add karo
@app.route('/add', methods=['GET', 'POST'])
def add_task():
    if request.method == 'POST':
        name = request.form['name']
        task = request.form['task']
        
        conn = get_db()
        conn.execute('INSERT INTO practice (name, task) VALUES (?, ?)', 
                     (name, task))
        conn.commit()
        conn.close()
        return redirect('/')
    return render_template('pradd_task.html')

if __name__ == '__main__':
    init_db()  # Table bana dega agar nahi hai
    app.run(debug=True)
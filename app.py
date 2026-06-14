from flask import Flask, redirect, render_template, request, url_for, flash
import sqlite3
from datetime import datetime

app = Flask(__name__)
app.secret_key = "hostel-visitor-2026"

def get_db():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def home():
    conn = get_db()
    visitors = conn.execute('SELECT * FROM visitors').fetchall()
    conn.close()

    total = len(visitors)
    inside = len([v for v in visitors if v['status'] == 'Inside'])
    return render_template('home.html', total=total, inside=inside)

@app.route('/records')
def records_page():
    conn = get_db()
    visitors = conn.execute('SELECT * FROM visitors ORDER BY id DESC').fetchall()
    conn.close()
    return render_template('records.html', visitors=visitors)

@app.route('/details/<int:id>')
def details(id):
    conn = get_db()
    visitor = conn.execute('SELECT * FROM visitors WHERE id = ?', (id,)).fetchone()
    conn.close()

    if visitor is None:
        flash('Visitor not found', 'danger')
        return redirect(url_for('records_page'))

    return render_template('details.html', visitor=visitor)

@app.route('/add_visitor', methods=['GET', 'POST'])
def add_visitor():
    if request.method == 'POST':
        visitor_name = request.form['visitor_name']
        student_name = request.form['student_name']
        room_number = request.form['room_number']
        purpose = request.form['purpose']

        if not visitor_name or not student_name or not room_number or not purpose:
            flash('Please complete all fields', 'danger')
            return render_template('add_visitor.html')

        in_time = datetime.now().strftime('%d-%m-%Y %I:%M %p')
        
        conn = get_db()
        conn.execute("""
            INSERT INTO visitors (visitor_name, student_name, room_number, purpose, in_time, status)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (visitor_name, student_name, room_number, purpose, in_time, 'Inside'))
        conn.commit()
        conn.close()

        flash(f'Visitor {visitor_name} added successfully', 'success')
        return redirect(url_for('records_page'))

    return render_template('add_visitor.html')

@app.route('/edit_visitor/<int:id>', methods=['GET', 'POST'])
def edit_visitor(id):
    conn = get_db()
    visitor = conn.execute('SELECT * FROM visitors WHERE id = ?', (id,)).fetchone()
    
    if visitor is None:
        conn.close()
        flash('Visitor not found', 'danger')
        return redirect(url_for('records_page'))

    if request.method == 'POST':
        visitor_name = request.form['visitor_name']
        student_name = request.form['student_name']
        room_number = request.form['room_number']
        purpose = request.form['purpose']
        
        conn.execute("""
            UPDATE visitors 
            SET visitor_name=?, student_name=?, room_number=?, purpose=?
            WHERE id=?
        """, (visitor_name, student_name, room_number, purpose, id))
        conn.commit()
        conn.close()
        
        flash('Visitor updated successfully', 'success')
        return redirect(url_for('records_page'))
    
    conn.close()
    return render_template('edit_visitor.html', visitor=visitor)

@app.route('/delete_visitor/<int:id>', methods=['POST'])
def delete_visitor(id):
    conn = get_db()
    conn.execute('DELETE FROM visitors WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    flash('Visitor deleted successfully', 'success')
    return redirect(url_for('records_page'))

@app.route('/checkout_visitor/<int:id>', methods=['POST'])
def checkout_visitor(id):
    conn = get_db()
    out_time = datetime.now().strftime('%d-%m-%Y %I:%M %p')
    
    cursor = conn.execute("""
        UPDATE visitors 
        SET status = 'Left', out_time = ? 
        WHERE id = ? AND status = 'Inside'
    """, (out_time, id))
    
    conn.commit()
    
    if cursor.rowcount == 0:
        flash('Visitor not found or already checked out', 'danger')
    else:
        flash('Visitor checked out successfully', 'success')
    
    conn.close()
    return redirect(url_for('records_page'))

@app.route('/search')
def search():
    query = request.args.get('q', '').strip()
    results = []

    if query:
        conn = get_db()
        search_term = f'%{query}%'
        results = conn.execute("""
            SELECT * FROM visitors 
            WHERE visitor_name LIKE ? 
               OR student_name LIKE ? 
               OR room_number LIKE ? 
               OR purpose LIKE ?
            ORDER BY id DESC
        """, (search_term, search_term, search_term, search_term)).fetchall()
        conn.close()

    return render_template('search_results.html', results=results, query=query)

@app.route('/about')
def about():
    return render_template('about.html')

if __name__ == '__main__':
    app.run(debug=True)
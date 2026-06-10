from flask import Flask, redirect, render_template, request, url_for, flash
import sqlite3
from datetime import datetime
from database import get_db, init_db

app = Flask(__name__)
app.secret_key = "hostel-visitor-2026"

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

@app.route('/delete/<int:id>', methods=['POST'])
def delete_visitor(id):
    conn = get_db()
    
    print(f"Someone clicked delete for ID: {id}")  # Step 1
    
    cursor = conn.execute('DELETE FROM visitors WHERE id = ?', (id,))
    conn.commit()
    
    print(f"Deleted. Rows affected: {cursor.rowcount}")  # Step 2
    
    conn.close()
    flash('Visitor deleted successfully', 'success')
    return redirect(url_for('records_page'))

@app.route('/checkout/<int:id>')  # <-- NAYA ROUTE
def checkout_visitor(id):
    conn = get_db()
    out_time = datetime.now().strftime('%d-%m-%Y %I:%M %p')
    cursor = conn.execute('UPDATE visitors SET out_time = ?, status = ? WHERE id = ?', 
                         (out_time, 'Outside', id))
    conn.commit()
    
    if cursor.rowcount == 0:
        flash('Visitor not found', 'danger')
    else:
        flash('Visitor checked out successfully', 'success')
    
    conn.close()
    return redirect(url_for('records_page'))

@app.route('/add_visitor', methods=['GET', 'POST'])
def add_visitor():
    if request.method == 'POST':
        visitor_name = request.form['visitor_name']
        student_name = request.form['student_name']
        room_number = request.form['room_number']
        purpose = request.form['purpose']
        
        if not visitor_name or not student_name or not room_number or not purpose:
            flash('Please complete all fields', 'danger')
            return render_template('add.html')
        
        in_time = datetime.now().strftime('%d-%m-%Y %I:%M %p')
        
        conn = get_db()
        conn.execute('''INSERT INTO visitors 
                     (visitor_name, student_name, room_number, purpose, in_time) 
                     VALUES (?, ?, ?, ?, ?)''',
                     (visitor_name, student_name, room_number, purpose, in_time))
        conn.commit()
        conn.close()
        
        print(f"Received new visitor: {visitor_name} for {student_name}")
        
        flash(f'Visitor {visitor_name} added successfully!', 'success')
        return redirect(url_for('records_page'))
    
    return render_template('add.html')

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
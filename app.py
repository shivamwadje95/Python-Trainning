from flask import Flask, redirect, render_template, request, url_for, flash, session
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
    visitors = conn.execute("SELECT * FROM visitors ORDER BY id DESC").fetchall()
    
    rooms = conn.execute("SELECT DISTINCT room_number FROM visitors ORDER BY room_number").fetchall()
    
    conn.close()
    
    total_count = len(visitors)
    inside_count = 0
    checkout_count = 0
    
    for v in visitors:
        if v['status'] == 'Inside':
            inside_count += 1
        else:
            checkout_count += 1
    
    return render_template('home.html', 
                         visitors=visitors,
                         total_count=total_count,
                         inside_count=inside_count,
                         checkout_count=checkout_count,
                         rooms=rooms,
                         name=session.get('name')) 

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form.get('name')
        if name:
            session['name'] = name
            flash(f'Welcome, {name}!', 'success')
            return redirect(url_for('home'))
        flash('Please enter a name', 'danger')
    return render_template('register.html')

@app.route('/logout')
def logout():
    session.pop('name', None)
    flash('Logged out successfully', 'info')
    return redirect(url_for('home'))

@app.route('/records')
def records():
    room = request.args.get('room')
    status = request.args.get('status')
    q = request.args.get('q')
    
    conn = get_db()
    query = "SELECT * FROM visitors WHERE 1=1"
    params = []
    
    if room:
        query += " AND room_number = ?"
        params.append(room)
    if status:
        query += " AND status = ?"
        params.append(status)
    if q:
        query += " AND visitor_name LIKE ?"  # fixed: was 'name'
        params.append(f"%{q}%")
    
    query += " ORDER BY id DESC"
    visitors = conn.execute(query, params).fetchall()
    conn.close()
    return render_template('records.html', visitors=visitors)

@app.route('/details/<int:id>')
def details(id):
    conn = get_db()
    visitor = conn.execute('SELECT * FROM visitors WHERE id = ?', (id,)).fetchone()
    conn.close()

    if visitor is None:
        flash('Visitor not found', 'danger')
        return redirect(url_for('records'))

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
        return redirect(url_for('records'))

    return render_template('add_visitor.html')

@app.route('/edit_visitor/<int:id>', methods=['GET', 'POST'])
def edit_visitor(id):
    conn = get_db()
    visitor = conn.execute('SELECT * FROM visitors WHERE id = ?', (id,)).fetchone()
    
    if visitor is None:
        conn.close()
        flash('Visitor not found', 'danger')
        return redirect(url_for('records'))

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
        return redirect(url_for('records'))
    
    conn.close()
    return render_template('edit_visitor.html', visitor=visitor)

@app.route('/delete_visitor/<int:id>', methods=['POST'])
def delete_visitor(id):
    conn = get_db()
    conn.execute('DELETE FROM visitors WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    flash('Visitor deleted successfully', 'success')
    return redirect(url_for('records'))

@app.route('/checkout_visitor/<int:id>', methods=['POST'])
def checkout_visitor(id):
    conn = get_db()
    out_time = datetime.now().strftime('%d-%m-%Y %I:%M %p')
    
    cursor = conn.execute("""
        UPDATE visitors 
        SET status = 'Checked Out', out_time = ? 
        WHERE id = ? AND status = 'Inside'
    """, (out_time, id))
    
    conn.commit()
    
    if cursor.rowcount == 0:
        flash('Visitor not found or already checked out', 'danger')
    else:
        flash('Visitor checked out successfully', 'success')
    
    conn.close()
    return redirect(url_for('records'))

@app.route('/filter')
def filter_visitors():
    room = request.args.get('room')
    purpose = request.args.get('purpose') 
    status = request.args.get('status')
    
    conn = get_db()
    query = "SELECT * FROM visitors WHERE 1=1"
    params = []
    
    if room:
        query += ' AND room_number = ?'
        params.append(room)
    if purpose:
        query += ' AND purpose = ?'
        params.append(purpose)
    if status:
        query += ' AND status = ?'
        params.append(status)
        
    query += " ORDER BY id DESC"
    visitors = conn.execute(query, params).fetchall()
    conn.close()
    
    return render_template('filter.html', 
                         visitors=visitors, 
                         selected_room=room, 
                         selected_purpose=purpose, 
                         selected_status=status)

@app.route('/search')
def search():
    q = request.args.get('q', '')
    conn = get_db()
    if q:
        search_term = f'%{q}%'
        visitors = conn.execute("""
            SELECT * FROM visitors 
            WHERE visitor_name LIKE ? OR room_number LIKE ? OR purpose LIKE ? OR student_name LIKE ?
            ORDER BY id DESC
        """, (search_term, search_term, search_term, search_term)).fetchall()
    else:
        visitors = conn.execute("SELECT * FROM visitors ORDER BY id DESC").fetchall()
    conn.close()
    return render_template('records.html', visitors=visitors)

@app.route('/about')
def about():
    return render_template('about.html', name=session.get('name'))

@app.context_processor
def inject_rooms():
    conn = get_db()
    rooms = conn.execute("SELECT DISTINCT room_number FROM visitors ORDER BY room_number").fetchall()
    conn.close()
    return dict(rooms=rooms)

if __name__ == '__main__':
    app.run(debug=True)
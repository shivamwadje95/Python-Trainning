from flask import Flask, render_template, request, redirect, url_for, flash
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'hostel-visitor-secret-key'

visitors = []

@app.route('/')
def home():
    total = len(visitors)
    inside = len([v for v in visitors if v['status'] == 'Inside'])
    return render_template('home.html', total=total, inside=inside)

@app.route('/records')
def records():
    return render_template('records.html', visitors=visitors)

@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        visitor_name = request.form.get('visitor_name')
        student_name = request.form.get('student_name')
        room_number = request.form.get('room_number')
        purpose = request.form.get('purpose')
        
        # Validation - empty check for assignment
        if not visitor_name or not student_name or not room_number or not purpose:
            flash('All fields are required!', 'danger')
            return redirect(url_for('add'))
        
        new_entry = {
            'id': len(visitors) + 1,
            'visitor': visitor_name,
            'student': student_name,
            'room': room_number,
            'purpose': purpose,
            'in_time': datetime.now().strftime('%I:%M %p'),
            'out_time': 'Still Inside',
            'status': 'Inside'
        }
        visitors.append(new_entry)
        flash('Visitor added successfully!', 'success')  # Flash message
        return redirect(url_for('records'))  # Redirect after submit
    
    return render_template('add.html')

@app.route('/about')  # THIS IS MISSING - ADD IT
def about():
    return render_template('about.html')

if __name__ == '__main__':
    app.run(debug=True)
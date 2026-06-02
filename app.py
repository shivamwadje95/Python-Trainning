from flask import Flask

app = Flask(__name__)

# project data - dictionary
visitor_log = [
    {"visitor_id": 101, "visitor_name": "Shivam Wadje", "student_name": "Amit Patil", "in_time": "10:30 AM", "status": "Checked Out", "purpose": "Parents Meeting"},
    {"visitor_id": 102, "visitor_name": "Priya Singh", "student_name": "Neha Gupta", "in_time": "11:45 AM", "status": "Checked In", "purpose": "Friend Visit"},
    {"visitor_id": 103, "visitor_name": "Zomato Delivery", "student_name": "Rohit Verma", "in_time": "01:20 PM", "status": "Checked Out", "purpose": "Food Delivery"},
    {"visitor_id": 104, "visitor_name": "Dr. Mehta", "student_name": "Hostel Warden", "in_time": "03:00 PM", "status": "Checked Out", "purpose": "Medical Checkup"},
    {"visitor_id": 105, "visitor_name": "Ajay Shinde", "student_name": "Pratik Mane", "in_time": "06:30 PM", "status": "Checked Out", "purpose": "Brother Visit"}
]

@app.route('/')
def home():
    # Create using HTML
    html = '<h1>Hostel Visitor Log Management System</h1>'
    html += '<p><b>Description:</b> This app tracks all hostel visitors with entry time, student details, and checkout status.</p>'
    html += f'<p><b>Total Visitors Today:</b> {len(visitor_log)}</p>'
    html += '<h3>Recent Visitors:</h3>'
    html += '<ul>'
    for visitor in visitor_log:
        html += f"<li>{visitor['visitor_name']} - Student: {visitor['student_name']} - Time: {visitor['in_time']} - Status: {visitor['status']}</li>"
    html += '</ul>'
    html += '<br><a href="/records">View All Records</a> | <a href="/about">About Project</a>'
    return html

@app.route('/about')
def about():
    return '<h1>About Project</h1><p>This Hostel Visitor Log system manages visitor entries for hostel security. It stores visitor ID, name, student visited, in-time, purpose and checkout status.</p><a href="/">Back to Home</a>'

@app.route('/records')
def records():
    html = '<h1>All Visitor Records</h1>'
    html += '<a href="/">Back to Home</a>'
    html += '<table border="1" cellpadding="8">'
    html += '<tr><th>ID</th><th>Visitor Name</th><th>Student Name</th><th>In Time</th><th>Purpose</th><th>Status</th></tr>'
    for visitor in visitor_log:
        html += f"<tr><td>{visitor['visitor_id']}</td><td>{visitor['visitor_name']}</td><td>{visitor['student_name']}</td><td>{visitor['in_time']}</td><td>{visitor['purpose']}</td><td>{visitor['status']}</td></tr>"
    html += '</table>'
    return html

if __name__ == "__main__":
    app.run(debug=True)
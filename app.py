from flask import Flask, render_template

app = Flask(__name__)

visitors = [
    {"id": 101, "name": "Rahul Sharma", "student": "Amit Kumar", "room": "B-204", "in_time": "10:30 AM", "purpose": "Friend visit"},
    {"id": 102, "name": "Priya Singh", "student": "Neha Gupta", "room": "G-112", "in_time": "02:15 PM", "purpose": "Family"},
    {"id": 103, "name": "Delivery Agent", "student": "Rohan Das", "room": "B-301", "in_time": "05:45 PM", "purpose": "Food delivery"}
]

@app.route('/')
def home():
    return render_template('home.html', project_name="Hostel Visitor Log")

@app.route('/records')
def records():
    return render_template('records.html', project_name="Hostel Visitor Log", visitors=visitors)

@app.route('/add')
def add_visitor():
    return render_template('add.html', project_name="Hostel Visitor Log")

@app.route('/record/<int:id>')
def visitor_detail(id):
    visitor = next((v for v in visitors if v["id"] == id), None)
    return render_template('record_detail.html', project_name="Hostel Visitor Log", visitor=visitor)

@app.route('/about')
def about():
    return render_template('about.html', project_name="Hostel Visitor Log")

if __name__ == '__main__':
    app.run(debug=True)
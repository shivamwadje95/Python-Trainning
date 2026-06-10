from flask import Flask

app = Flask(__name__)

# List of dictionaries (Visitor Records)
visitors = [
    {
        "id": 1,
        "visitor_name": "Rahul Patil",
        "student_name": "Shivam Wadje",
        "purpose": "Meeting",
        "in_time": "10:00 AM",
        "status": "Checked Out"
    },
    {
        "id": 2,
        "visitor_name": "Ajay Shinde",
        "student_name": "Karan Jadhav",
        "purpose": "Document Delivery",
        "in_time": "11:30 AM",
        "status": "Checked Out"
    },
    {
        "id": 3,
        "visitor_name": "Sneha Patil",
        "student_name": "Rohit More",
        "purpose": "Family Visit",
        "in_time": "1:00 PM",
        "status": "Inside"
    },
    {
        "id": 4,
        "visitor_name": "Amit Kale",
        "student_name": "Krushna Rathod",
        "purpose": "Meeting",
        "in_time": "4:00 PM",
        "status": "Checked Out"
    },
    {
        "id": 5,
        "visitor_name": "Priya Jadhav",
        "student_name": "Ajay Shinde",
        "purpose": "Family Visit",
        "in_time": "6:30 PM",
        "status": "Inside"
    }
]

# Route 1 - Home Page
@app.route("/")
def home():
    return """
    <h1>🏨 Hostel Visitor Log System</h1>
    <p>
    This project helps hostel management maintain visitor records,
    monitor visitor entry, improve security, and keep track of
    visitors currently inside the hostel.
    </p>

    <h3>Available Pages</h3>
    <ul>
        <li><a href='/records'>Visitor Records</a></li>
        <li><a href='/inside'>Visitors Inside Hostel</a></li>
        <li><a href='/about'>About Project</a></li>
    </ul>
    """

# Route 2 - Records Page
@app.route("/records")
def records():

    html = """
    <h1>📋 Visitor Records</h1>
    <table border='1' cellpadding='8'>
        <tr>
            <th>ID</th>
            <th>Visitor Name</th>
            <th>Student Name</th>
            <th>Purpose</th>
            <th>In Time</th>
            <th>Status</th>
        </tr>
    """

    for v in visitors:
        html += f"""
        <tr>
            <td>{v['id']}</td>
            <td>{v['visitor_name']}</td>
            <td>{v['student_name']}</td>
            <td>{v['purpose']}</td>
            <td>{v['in_time']}</td>
            <td>{v['status']}</td>
        </tr>
        """

    html += "</table><br><a href='/'>Back to Home</a>"
    return html

# Route 3 -  Project Route
@app.route("/inside")
def inside():
    html = """
    <h1>🚪 Visitors Currently Inside Hostel</h1>
    <ul>
    """

    for v in visitors:
        if v["status"] == "Inside":
            html += f"<li>{v['visitor_name']} - Visiting {v['student_name']}</li>"

    html += """
    </ul>
    <a href='/'>Back to Home</a>
    """
    return html

# Route 4 - About Page
@app.route("/about")
def about():
    return """
    <h1>ℹ️ About Hostel Visitor Log</h1>
    <p>
    The Hostel Visitor Log System is designed to record visitor
    information, track entry details, and improve hostel security.
    It helps wardens quickly identify who is currently inside the hostel.
    </p>

    <a href='/'>Back to Home</a>
    """

if __name__ == "__main__":
    app.run(debug=True)
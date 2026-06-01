
# Main  Dictionary 
hostel_info = {
    "hostel_name": "Sunrise Boys Hostel",
    "location": "Pune",
    "warden_name": "Mr. Deshmukh",
    "total_rooms": 120,
    "occupied_rooms": 98,
    "status": "Open"
}

# List of Dictionaries (5 Visitor Records)
visitors = [
    {
        "visitor_id": 101,
        "visitor_name": "Shivam Wadje",
        "student_name": "Amit Patil",
        "visit_date": "01-06-2026",
        "in_time": "10:00 AM",
        "status": "Checked Out"
    },
    {
        "visitor_id": 102,
        "visitor_name": "Karan Jadhav",
        "student_name": "Rohit Shinde",
        "visit_date": "01-06-2026",
        "in_time": "11:30 AM",
        "status": "Checked In"
    },
    {
        "visitor_id": 103,
        "visitor_name": "Rahul Patil",
        "student_name": "Sagar More",
        "visit_date": "01-06-2026",
        "in_time": "02:15 PM",
        "status": "Checked Out"
    },
    {
        "visitor_id": 104,
        "visitor_name": "Krushna Rathod",
        "student_name": "Vikas Jadhav",
        "visit_date": "01-06-2026",
        "in_time": "04:00 PM",
        "status": "Checked In"
    },
    {
        "visitor_id": 105,
        "visitor_name": "Ajay Shinde",
        "student_name": "Pratik Mane",
        "visit_date": "01-06-2026",
        "in_time": "06:30 PM",
        "status": "Checked Out"
    }
]

#  Second Dictionary Type
room_info = {
    "A101": "Occupied",
    "A102": "Vacant",
    "B201": "Occupied",
    "B202": "Vacant",
    "C301": "Occupied"
}


def get_status():
    return hostel_info["status"]

#  Search Visitor Record
def search_records(visitor_name):
    for visitor in visitors:
        if visitor["visitor_name"].lower() == visitor_name.lower():
            return visitor
    return "Visitor not found"


print("HOSTEL INFORMATION")
for key, value in hostel_info.items():
    print(f"{key}: {value}")


print("\nHostel Status:", get_status())


print("\nVISITOR RECORDS")
for visitor in visitors:
    print("-" * 40)
    for key, value in visitor.items():
        print(f"{key}: {value}")


print("\nROOM INFORMATION")
for room, status in room_info.items():
    print(f"{room}: {status}")

# Search Example
print("\nSEARCH RESULT")
result = search_records("Shivam Wadje")
print(result)

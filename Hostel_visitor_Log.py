visitor_name = ["Shivam Wadje", "Karan Jadhav", "Rahul Patil", "Krushna Rathod", "Ajay Shinde"]
visitor_In_Time = ["10:00 AM", "11:30 AM", "04:15 PM", "8:00 PM", "6:30 PM"]

def get_status(time):
    hour = int(time.split(":")[0])

    if "PM" in time and hour != 12:
        hour += 12

    if "AM" in time and hour == 12:
        hour = 0

    if hour < 18:
        return "Allowed"
    else:
        return "Late Entry"

print("***** HOSTEL VISITOR LOG REPORT *****")
print("{:<20} {:<15} {:<15}".format("Visitor Name", "IN Time", "Status"))
print("-" * 50)

for i in range(len(visitor_name)):
    name = visitor_name[i]
    time = visitor_In_Time[i]
    status = get_status(time)

    print("{:<20} {:<15} {:<15}".format(name, time, status))

print("-" * 50)
print("Total Visitors today:", len(visitor_name))


A=int(input("Ente a marks A:"))
B=int(input("Enter a marks B:"))
C=int(input("Enter a marks C:"))
D=int(input("Enter a marks D:"))
E=int(input("Enter a marks E:"))
total=A+B+C+D+E
percentage=total/5 
print("total marks=",total)
print("percentage=",percentage)
if percentage>=75:
    print("Result is: distinction")
elif percentage>=60: 
    print("Result is: First class ")
elif percentage>=45:
    print("Result is: pass") 
else:
    print("Result is: Fail") 

try:
    mark = float(input("Enter mark (0-100): "))
except ValueError:
    print("That is not a number")
    exit()

if mark < 0 or mark > 100:
    print("Mark must be between 0 and 100")
elif mark == 0:
    print("N/S")
elif mark < 40:
    print("F")
elif mark < 50:
    print("D")
elif mark < 60:
    print("C")
elif mark < 70:
    print("B")
elif mark < 80:
    print("A")
else:
    print("A*")

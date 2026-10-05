while True:
    first = input("First number (or quit): ")
    if first == "quit":
        break
    second = input("Second number (or quit): ")
    if second == "quit":
        break

    a = int(first)
    b = int(second)

    if a > b:
        print(a, "is bigger than", b)
    elif b > a:
        print(b, "is bigger than", a)
    else:
        print("Both numbers are the same")

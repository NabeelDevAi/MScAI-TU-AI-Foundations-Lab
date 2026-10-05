name = input("Name: ")
age = int(input("Age: "))
country = input("Country of citizenship: ")

if age < 18:
    print(name + " is not yet old enough to vote")
elif country.lower() in ["uk", "britain"]:
    print(name + " is entitled to vote")
else:
    print(name + " is not entitled to vote")

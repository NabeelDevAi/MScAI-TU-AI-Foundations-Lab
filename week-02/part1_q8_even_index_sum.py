numbers = [14, 5, 19, 20, 21, 66, 89]
total = 0

for i in range(len(numbers)):
    if i % 2 == 0:
        total += numbers[i]

print("Sum:", total)

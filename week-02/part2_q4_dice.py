import random

counts = [0] * 11

for i in range(100):
    total = random.randint(1, 6) + random.randint(1, 6)
    counts[total - 2] += 1

print("Distribution Chart")
print("Score Rolls")
for i in range(11):
    print(str(i + 2).ljust(6) + str(counts[i]).ljust(6) + "*" * counts[i])

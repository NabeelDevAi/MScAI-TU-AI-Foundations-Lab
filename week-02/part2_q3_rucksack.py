import random

rucksack = ["Water flask", "Cheese", "Gold coins", "Handkerchief", "Tinderbox",
            "Scrolls", "Dagger", "Rope", "Nuts", "Pipe", "Tobacco",
            "Wine skin", "Herbs", "Axe"]

rucksack.sort()
print(rucksack)
print("Items:", len(rucksack))

rucksack.append("Gems")
rucksack.append("Necklace")
rucksack.sort()
print(rucksack)

for i in range(5):
    stolen = random.choice(rucksack)
    rucksack.remove(stolen)
    print("Thief took", stolen)

print(rucksack)

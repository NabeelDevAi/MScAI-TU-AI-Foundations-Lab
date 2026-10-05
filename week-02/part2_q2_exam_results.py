# TUT_datafile.py wasn't available, so sample data is here
results = [
    ["Alice", 82], ["Bob", 65], ["Charlie", 45], ["Diana", 38],
    ["Ethan", 71], ["Fiona", 29], ["George", 55], ["Hannah", 90],
    ["Ian", 34], ["Jack", 60],
]


def grade(mark):
    if mark >= 70:
        return "Distinction"
    elif mark >= 60:
        return "Merit"
    return "Pass"


def pass_list(results):
    print("Pass list")
    for name, mark in results:
        if mark >= 40:
            print(name, mark, grade(mark))


def fail_list(results):
    print("\nFail list")
    for name, mark in results:
        if mark < 30:
            print(name, mark, "Fail")
        elif mark < 40:
            print(name, mark, "Fail - resubmission allowed")


def stats(results):
    best = max(results, key=lambda r: r[1])
    worst = min(results, key=lambda r: r[1])
    average = sum(r[1] for r in results) / len(results)
    return best, worst, average


def above_below(results, average):
    above = 0
    below = 0
    for name, mark in results:
        if mark > average:
            above += 1
        elif mark < average:
            below += 1
    return above, below


pass_list(results)
fail_list(results)

best, worst, average = stats(results)
print("\nHighest mark:", best[1], "by", best[0])
print("Range:", worst[1], "to", best[1])
print("Average:", average)

above, below = above_below(results, average)
print("Above average:", above)
print("Below average:", below)

import random


def make_list():
    return [random.randint(0, 99) for i in range(20)]


def second_largest_smallest(nums):
    s = sorted(set(nums))
    return s[-2], s[1]


nums = make_list()
print(nums)
big, small = second_largest_smallest(nums)
print("Second largest:", big)
print("Second smallest:", small)

third_highest = sorted(set(nums))[-3]
nums = [n for n in nums if n <= third_highest]
print("After removing above third highest:", nums)

nums = make_list()
print("\nNew list:", nums)
nums.insert(10, 50)

first_half = nums[:10]
second_half = nums[11:]

moved_up = [n for n in first_half if n > 50]
first_half = [n for n in first_half if n <= 50]
second_half += moved_up

moved_down = [n for n in second_half if n < 50]
second_half = [n for n in second_half if n >= 50]
first_half += moved_down

nums = first_half + [50] + second_half
print("Result:", nums)

first_num = int(input("First number: "))
second_num = int(input("Second number: "))
third_num = int(input("Third number: "))

if first_num > second_num:
    first_num, second_num = second_num, first_num
if second_num > third_num:
    second_num, third_num = third_num, second_num
if first_num > second_num:
    first_num, second_num = second_num, first_num

print(first_num, second_num, third_num)

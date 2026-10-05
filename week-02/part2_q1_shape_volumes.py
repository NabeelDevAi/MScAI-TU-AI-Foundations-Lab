import math


def sphere(r):
    return 4 / 3 * math.pi * r ** 3


def cylinder(r, h):
    return math.pi * r ** 2 * h


def cone(r, h):
    return 1 / 3 * math.pi * r ** 2 * h


print("Sphere:", sphere(3))
print("Cylinder:", cylinder(3, 5))
print("Cone:", cone(3, 5))

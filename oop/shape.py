#!/usr/bin/env python
#-*- coding: utf-8 -*-

import math

class Shape2d:
    def area(self):
        raise NotImplementedError()

class Square(Shape2d):
    def __init__(self, width):
        self.width = width

    def area(self):
        return self.width ** 2

class Disk(Shape2d):
    def __init__(self, radius):
        self.radius = radius

    def area(self):
        return math.pi * self.radius ** 2

shapes = [Square(2), Disk(3)]
print([s.area() for s in shapes])
s = Shape2d()
try:
    print(s.area)
except NotImplementedError as e:
    print(e)

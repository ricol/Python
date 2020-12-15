#!/usr/bin/env python
#-*- coding: utf-8 -*-

import math

for a in range(100):
    for b in range(100):
        z = (a ** 2 + b ** 2) / (a * b * 1.0 + 1)
        square = math.sqrt(z)
        print("a = %f, b = %f, z = %f, square = %f" % (a, b, z, square))

print("end.")

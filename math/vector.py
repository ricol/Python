#!/usr/bin/env python
#-*- coding: utf-8 -*-

import numpy as np

x = [1, 2, 3]
y = [4, 5, 6]

print(type(x))
print(x + y)
z = np.add(x, y)
print(z)
print(type(z))
mul = np.cross(x, y)
print(mul)
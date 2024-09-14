#!/usr/bin/env python
#-*- coding: utf-8 -*-

import pylab
from scipy import arange
from scipy import cos
from scipy import exp
from scipy.optimize import fmin

def f(x):
    return cos(x) - 3 * exp(-(x - 0.2) ** 2)

minimum1 = fmin(f, 1.0)
print("Start search at x = 1.0, minimum is: ", minimum1)
minimum2 = fmin(f, 2.0)
print("Start search at x = 2.0, minimum is: ", minimum2)

x = arange(-10, 10, 0.1)
y = f(x)
pylab.plot(x, y)
pylab.xlabel('x')
pylab.grid()
pylab.axis([-5, 5, -2.2, 0.5])

pylab.show()

print("end.")

#!/usr/bin/env python
#-*- coding: utf-8 -*-

print("Newton Methods Demonstration")

def f(x):
    return 3.0 * x * x * x + 2.0 * x * x + x + 1.0

def fd(x):
    return 9.0 * x * x + 4.0 * x + 1.0

def nextX(x):
    return x - f(x) / fd(x)

x = 100.0
times = 1000
t = 0
while t < times:
    t += 1
    n = nextX(x)
    dif = abs(n - x)
    print("Times: [%d] -> New Value: [%f] -> Dif: [%f]" % (t, x, dif))
    x = n
    if dif <= 0:
        break
print("Answer: %f" % x)

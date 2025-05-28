#!/usr/bin/env python
#-*- coding: utf-8 -*-

def derivative(f, h):
    return lambda x: (f(x + h) - f(x)) / h

def fun(x):
    return 3 * x ** 2 + 5

def ans(x):
    return 6 * x

h = 1.0e-7
der = derivative(fun, h)
x = 5.0

print('----------------------------------------')
print('                          Appro.  Actual')
print('  x     f(x)      h        f\'(x) f\'(x)')
print('----------------------------------------')

while x < 5.1:
    print('{:.5f} {:.5f} {:.8f} {:.5f} {:.5f}'.format(x, fun(x), h, der(x), ans(x)))
    x += 0.01
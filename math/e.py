#!/usr/bin/env python
#-*- coding: utf-8 -*-

from os import sys

def factorial(n):
    if n <= 1:
        return 1
    else:
        return factorial(n - 1) * n

if len(sys.argv) > 1:
    num = int(sys.argv[1])
else:
    num = 100
e = 0.0
print("Calculating e...")
print("num = %d" % num)
for i in range(num + 1):
    e += 1.0 / factorial(i)
print("result: %f" % e)
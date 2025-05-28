#!/usr/bin/env python
#-*- coding: utf-8 -*-

def factorial(n):
    return 1 if n <= 1 else n * factorial(n - 1)

for i in range(30):
    print("%d! = %d" % (i, factorial(i)))
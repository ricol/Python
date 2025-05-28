#!/usr/bin/env python
#-*- coding: utf-8 -*-

import sys

def fibonacci(n):  #generator function
    a, b, counter = 0, 1, 0
    while True:
        if (counter > n):
            return
        yield a
        a, b = b, a + b
        counter += 1

f = fibonacci(5)  #f is iterator object

while True:
    try:
        print((next(f)))
    except StopIteration:
        break

def fib(n):
    a, b, counter = 0, 1, 0
    while True:
        if (counter > n):
            return
        yield a

        a, b = b, a + b
        counter += 1

f = fib(10)
while True:
    try:
        print((next(f)))
    except StopIteration:
        sys.exit()
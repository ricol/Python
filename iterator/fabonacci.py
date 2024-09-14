#!/usr/bin/env python
#-*- coding: utf-8 -*-

def fibonacci():
    a = 0
    b = 1
    while True:
        yield a
        future = a + b
        a = b
        b = future

def fibonacci_new():
    a = 0
    b = 1
    while True:
        yield a
        a, b = b, a + b

n = 0
MAX = 10
print("demo1...")
a = fibonacci()
while n < MAX:
    print(a.next())
    n += 1
print("demo2...")
n = 0
b = fibonacci_new()
while n < MAX:
    print(b.next())
    n += 1
print("done")

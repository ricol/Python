#!/usr/bin/env python
#-*- coding: utf-8 -*-

def fibonacci():
    a, b = 0, 1
    while True:
        yield a
        a, b = b, a + b

if __name__ == "__main__":
    MAX = 100000
    print("Printing fibonaccis (<%d)" % MAX)
    print("*" * 10)
    for f in fibonacci():
        if f > MAX: break
        print(f)
    print("*" * 10)

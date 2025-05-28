#!/usr/bin/env python
#-*- coding: utf-8 -*-

import os

cache = {}

def f(n):
    if n in cache:
        return cache[n]

    result = 1
    if n >= 2:
        result = f(n - 1) + f(n - 2)
    cache[n] = result
    return result

if __name__ == "__main__":
    if len(os.sys.argv) <= 1:
        print("usage: f <num>")
        exit()
    try:
        num = int(os.sys.argv[1])
        for n in range(1, num + 1):
            print f(n),
    except Exception as e:
        print("invalid number: %s" % e)
        exit()
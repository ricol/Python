#!/usr/bin/env python
#-*- coding: utf-8 -*-

from time import time

def fibonacci(n):
    a, b, i = 0, 1, 0
    yield i, a, 0
    while i < n:
        i += 1
        yield i, b, b * 1.0 / a if a > 0 else 0
        a, b = b, a + b

start_time = time()
for i, f, ratio in fibonacci(200):
    print("%d: %d -> %.20f" % (i, f, ratio))
end_time = time()
elapsed = end_time - end_time
print("time: %f" % elapsed)
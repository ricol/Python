#!/usr/bin/env python
#-*- coding: utf-8 -*-

import random
from time import time
import funs

def sort(data, numDigits):
    queues = [[] for _ in range(10)]

    column = 1
    for _ in range(numDigits):
        for k in data:
            digit = (k // column) % 10
            queues[digit].append(k)

        i = 0
        for q in queues:
            while len(q) > 0:
                data[i] = q.pop(0)
                i += 1

        column *= 10

LEN = int(1e5)
print "generating..."
data = [random.randint(0, LEN) for _ in range(LEN)]
start = time()
print "sorting..."
sort(data, 6)
print "complete."
print "time: " + str(time() - start) + " seconds"
print "checking..." + str(funs.isSorted(data))
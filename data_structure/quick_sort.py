#!/usr/bin/env python
#-*- coding: utf-8 -*-

import random
import funs
from time import time

def quick_sort(data):
    if len(data) <= 1: return data
    m = len(data) / 2
    pivot = data[m]
    left, right = [], []
    for i in range(len(data)):
        if i == m: continue
        if data[i] < pivot: left.append(data[i])
        else: right.append(data[i])
    return quick_sort(left) + [pivot] + quick_sort(right)

if __name__ == "__main__":
    LEN = int(1e5)
    print 'generating...'
    data = [random.randint(0, LEN) for _ in range(LEN)]
    start = time()
    print 'sorting...'
    sorted = quick_sort(data)
    print 'complete with time cost: ' + str(time() - start) + " seconds"
    print 'checking...' + str(funs.isSorted(sorted))
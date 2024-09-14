#!/usr/bin/env python
#-*- coding: utf-8 -*-

import random
from time import time
import funs

def heapify(data, n, i):
    # Find largest among root and children
    largest = i
    l = 2 * i + 1
    r = l + 1

    if l < n and data[i] < data[l]:
        largest = l

    if r < n and data[largest] < data[r]:
        largest = r

    # If root is not largest, swap with largest and continue heapifying
    if largest != i:
        data[i], data[largest] = data[largest], data[i]
        heapify(data, n, largest)

def heapSort(data):
    n = len(data)

    # Build max heap
    for i in range(n//2, -1, -1):
        heapify(data, n, i)

    # funs.show_tree(data)
    print "verify heap..." + str(funs.isHeap(data, 0))

    for i in range(n-1, 0, -1):
        # Swap
        data[i], data[0] = data[0], data[i]

        # Heapify root element
        heapify(data, i, 0)

if __name__ == "__main__":
    LEN = int(1e5)
    print 'generating data...'
    data = [random.randint(0, LEN) for _ in range(LEN)]
    print 'sorting...'
    start = time()
    heapSort(data)
    print 'complete with time cost: ' + str(time() - start) + " seconds."
    print 'verifying...' + str(funs.isSorted(data))
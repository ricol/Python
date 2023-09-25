#!/usr/bin/env python
#-*- coding: utf-8 -*-

import random

def binary_search(list, data, start, end):
    if end < start: return -1
    mid = (end - start) / 2 + start
    if data < list[mid]:
        return binary_search(list, data, start, mid - 1)
    elif data > list[mid]:
        return binary_search(list, data, mid + 1, end)
    else:
        return mid

SIZE = int(1e5)
data = [random.randint(1, SIZE) for _ in range(SIZE)]
data.sort()
num = random.randint(1, SIZE)
print("searching for %d..." % num)
result = binary_search(data, num, 0, len(data) - 1)
print("found at: %d" % result if result >= 0 else "not found!")
print("validating: data[%d] = %d" % (result, data[result]) if result >= 0 else "end")

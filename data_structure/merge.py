#!/usr/bin/env python
#-*- coding: utf-8 -*-

import random

def merge_sort(data):
    def merge(l, r):
        s, l_index, r_index = [], 0, 0

        while l_index < len(l) and r_index < len(r):
            if l[l_index] > r[r_index]:
                s.append(r[r_index])
                r_index += 1
            else:
                s.append(l[l_index])
                l_index += 1

        while l_index < len(l):
            s.append(l[l_index])
            l_index += 1

        while r_index < len(r):
            s.append(r[r_index])
            r_index += 1

        return s

    def sort(data):
        if len(data) <= 1:
            return data

        middle = len(data) / 2
        left = sort(data[:middle])
        right = sort(data[middle:])
        return merge(left, right)

    return sort(data)

data = []
for _ in range(100):
    data.append(random.randint(0, 100))
print(data)
print("sorting...")
sorted = merge_sort(data)
print(sorted)
print("end.")

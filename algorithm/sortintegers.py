#!/usr/bin/env python
#-*- coding: utf-8 -*-

import random

def bubble_sort(data):
    for i in range(len(data) - 1):
        for j in range(len(data) - 1, i, -1):
            if data[j] < data[j - 1]:
                data[j], data[j - 1] = data[j - 1], data[j]
    return data

def insert_sort(data):
    if len(data) <= 1: return data
    for i in range(len(data)):
        for j in range(i + 1, len(data)):
            if data[i] > data[j]: data[i], data[j] = data[j], data[i]

    return data 

def quick_sort(data):
    if len(data) <= 1: return data
    mid = data[len(data) / 2]
    left, right = [], []
    data.remove(mid)

    for d in data:
        if d < mid: left.append(d)
        elif d > mid: right.append(d)

    return quick_sort(left) + [mid] + quick_sort(right) 

def validate(data):
    for i in range(len(data) - 1):
        if data[i] > data[i + 1]: return False
    return True

def generate(num=10000):
    return [random.randint(1, num) for _ in range(num)]

if __name__ == "__main__":
    for fun in [quick_sort, bubble_sort, insert_sort]:
        print("Generating data...")
        data = generate()
        print("Total: %d" % len(data))
        print("Sorting %s..." % fun)
        sorted_data = fun(data)
        print("Validing...%s" % (validate(sorted_data)))

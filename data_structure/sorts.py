#!/usr/bin/env python
#-*- coding: utf-8 -*-

import random
import funs

def quick_sort(list):
    if len(list) <= 1:
        return list

    mid = list[len(list) / 2]
    left, right = [], []
    list.remove(mid)

    for data in list:
        if data <= mid:
            left.append(data)
        elif data > mid:
            right.append(data)

    return quick_sort(left) + [mid] + quick_sort(right)

def bubble_sort(list):
    for i in range(len(list) - 1, -1, -1):
        for j in range(i):
            if list[j] > list[j + 1]:
                list[j], list[j + 1] = list[j + 1], list[j]
    return list

def quick_sort_lamda(list):
    sort = lambda array: array if len(array) <= 1 else sort([item for item in array[1:] if item <= array[0]]) + [array[0]] + sort([item for item in array[1:] if item > array[0]])
    sort(list)
    return list

def generate_data():
    NUM = int(1e3)
    data = [int(random.random() * NUM) for _ in range(NUM)]
    return data

if __name__ == "__main__":
    for fun in [quick_sort, quick_sort_lamda, bubble_sort]:
        print("Generating data...")
        data = generate_data()
        print("Total: %d" % len(data))
        print("Testing %s..." % fun)
        sorted_data = fun(data)
        print("Validating...%s...total: %d" % (funs.isSorted(sorted_data), len(sorted_data)))
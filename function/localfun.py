#!/usr/bin/env python3
#-*- coding: utf-8 -*-

def create_counter(n):
    count = 0

    def counter():
        nonlocal count
        if count < n:
            count += 1
        return count

    return counter

ctr = create_counter(4)
print(ctr())
print(ctr())
print(ctr())
print(ctr())
print(ctr())
print(ctr())
print(ctr())
print(ctr())
print(ctr())

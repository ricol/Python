#!/usr/bin/env python
#-*- coding: utf-8 -*-

def factors(n):
    results = []
    for k in range(1, n + 1):
        if n % k == 0:
            results.append(k)
    return results

def factors_iterator(n):
    for k in range(1, n + 1):
        if n % k == 0:
            yield k

def factors_iterator_new(n):
    k = 1
    while k * k < n:
        if n % k == 0:
            yield k
            yield n // k
        k += 1
    if k * k == n:
        yield k

n = 100
print("demo factors...")
print(factors(n))
print("demo factor iterators...")
f = factors_iterator(n)
for a in f:
    print(a)
print("demo factor iterators new...")
f = factors_iterator_new(n)
for a in f:
    print(a)
print("done.")
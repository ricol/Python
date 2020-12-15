#!/usr/bin/env python
#-*- coding: utf-8 -*-

print("Demo1...")
def f(x, l=[]):
    for i in range(x):
        l.append(i * i)
    print(l)

f(2)
f(3, [3, 2, 1])
f(3)

print("Demo2...")
l_mem = []
l = l_mem           # the first call
for i in range(2):
    l.append(i * i)
print(l)             # [0, 1]
l = [3, 2, 1]         # the second call
for i in range(3):
    l.append(i * i)
print(l)             # [3, 2, 1, 0, 1, 4]

l = l_mem           # the third call
for i in range(3):
    l.append(i * i)
print(l)             
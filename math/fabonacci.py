#!/usr/bin/env python
#-*- coding: utf-8 -*-

def fab(max):
    n, a, b = 0, 0, 1
    while n < max:
        print(b)
        a, b = b, a + b
        n += 1

def fab2(max):
    n, a, b = 0, 0, 1
    l = []
    while n < max:
        l.append(b)
        a, b = b, a + b
        n += 1
    return l

class Fab:
    def __init__(self, max):
        self.max = max
        self.n, self.a, self.b = 0, 0, 1

    def __iter__(self):
        return self

    def __next__(self):
        if self.n < self.max:
            r = self.b
            self.a, self.b = self.b, self.a + self.b
            self.n = self.n + 1
            return r
        raise StopIteration()

def fab3(max):
    n, a, b = 0, 0, 1
    while n < max:
        yield b
        a, b = b, a + b
        n += 1

MAX = 10
fab(MAX)
print(fab2(MAX))
for n in Fab(MAX):
    print(n)

for n in fab3(MAX):
    print(n)
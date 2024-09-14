#!/usr/bin/env python
#-*- coding: utf-8 -*-

import numpy
import time

N = 10000000

def timeit(f, args):
    starttime = time.time()
    y = f(*args) # use tuple args as input arguments 
    endtime = time.time()
    return endtime - starttime, y

def forloop1(N):
    s = 0
    for i in range(N):
        s += float(i) * float(i) 
    return s

def forloop2(N): 
    y = [0] * N
    for i in range(N):
        y[i] = float(i) ** 2
    return sum(y)

def listcomp(N):
    return sum([float(x) * x for x in range(N)])

def numpy_(N):
    return numpy.sum(numpy.arange(0, N, dtype='d') ** 2)

print("N =", N)
forloop1, res = timeit(forloop1, (N,))
print("forloop1", forloop1, "seconds")
forloop2, res = timeit(forloop2, (N,))
print("forloop2", forloop2, "seconds")
listcomp, res = timeit(listcomp, (N,))
print("listcomp", listcomp, "seconds")
numpy, res = timeit(numpy_, (N,))
print("numpy", numpy, "seconds")

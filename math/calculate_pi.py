#!/usr/bin/env python
#-*- coding: utf-8 -*-

from math import sqrt
import os

def calculate(n, l):
    a = l / 2.0
    b = sqrt(1 - a ** 2)
    c = sqrt((1 - b) ** 2 + a ** 2)
    pi = n * c
    return 2 * n, c, pi

def test(start, side, t):
    n, l = start, side
    print "Start with %d polygon (side: %f)..." % (n, l)
    for i in range(t):
        n, l, pi = calculate(n, l)
        print "[%d] polygon: %d, side: %f -> pi: %f" % (i, n, l, pi)

if __name__ == '__main__':
    if len(os.sys.argv) <= 1:
        print "Usage: calculate_pi.py <times>"
        exit()
    t = int(os.sys.argv[1])
    test(4, sqrt(2), t)
    test(6, 1, t)

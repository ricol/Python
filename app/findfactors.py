#!/usr/bin/env python
#-*- coding: utf-8 -*-

import os

n = 1

if len(os.sys.argv) <= 1:
    print("usage: findfactors <num>")
    exit()
MAX = int(os.sys.argv[1])
print "Find all factors of number from 1 to ", MAX
while n <= MAX:
    factor = 1
    print str(n) + ": ",
    while factor <= n:
        if n % factor == 0:
            print factor, 
        factor += 1
    print
    n += 1

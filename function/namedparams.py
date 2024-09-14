#!/usr/bin/env python
#-*- coding: utf-8 -*-

def process(a, b, c):
    print('a = %d, b = %d, c = %d' % (a, b, c))

x = 14
process(1, 2, 3)
process(a=10, b=20, c=30)
process(a=200, c=300, b=100)
process(c=3000, a=1000, b=2000)
process(10000, c=3000, b=20000)

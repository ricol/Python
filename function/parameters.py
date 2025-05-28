#!/usr/bin/env python
#-*- coding: utf-8 -*-

def f(a, b, c):
    print('a = %d, b = %d, c = %d' % (a, b, c))

f(1, 2, 3)
dict = {}
dict['a'] = 11
dict['b'] = 22
dict['c'] = 33
f( ** dict)
f( ** {'a': 10, 'b': 20, 'c': 30})
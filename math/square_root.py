#!/usr/bin/env python
#-*- coding: utf-8 -*-

def square_root(val):
	""" Computer an approximation of the square root of x """
	root = 1.0
	diff = root * root - val
	while diff > 1e-8 or diff < -1e-8:
		root = (root + val / root) / 2
		diff = root * root - val
	return root

from math import sqrt
d = 1.0
while d <= 10.0:
	print('{0:6.1f}: {1:16.8f} {2:16.8f}'.format(d, square_root(d), sqrt(d)))
	d += 0.5
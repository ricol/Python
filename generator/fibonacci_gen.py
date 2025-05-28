#!/usr/bin/env python
#-*- coding: utf-8 -*-

def fib(max):
	a, b = 0, 1

	while b < max:
		yield b
		a, b = b, a + b

max = 100
g = fib(max)
try:
	print("print fabonacci sequence until %d" % max)
	for e in g:
		print(e)
except KeyboardInterrupt:
	print("Calculation stopped")
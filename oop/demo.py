#!/usr/bin/env python
#-*- coding: utf-8 -*-

class A:
	def __init__(self, x):
		self.x = x

class B:
	def __init__(self, y):
		self.y = y

class C(A, B):
	def __init__(self, x, y, z):
		A.__init__(self, x)
		B.__init__(self, y)
		self.z = z

class D:
	def __init__(self, **args):
		for k in args:
			print("args[%s]=%s" % (k, args[k]))

a = A(1)
b = B(2)
c = C(1, 2, 3)
print(a.x)
print(b.y)
print(c.x, c.y, c.z)
d = D(x = 1, y = 2, z = 3, a = 'ricol', b = True, c = 1.2)

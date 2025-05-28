#!/usr/bin/env python
#-*- coding: utf-8 -*-

class A:

	def __init__(self, index, num):
		self.data = [0 for _ in range(10)]
		self.data[index] = num

	def __str__(self):
		return "%s" % self.data

	def __len__(self):
		return len(self.data)

	def __getitem__(self, index):
		return self.data[index]

	def __setitem__(self, index, value):
		self.data[index] = value

	def __contains__(self, num):
		return num in self.data

if __name__ == "__main__":
	a = A(2, 2)
	a[1] = 3
	a[3] = 4
	print(a)
	print(len(a))
	print(a[2])
	print(2 in a)
	print(5 in a)
	for i in a:
		print(i)
#!/usr/bin/env python
#-*- coding: utf-8 -*-

class Seq:
	def __init__(self):
		self.x = 0

	def next(self):
		self.x += 1
		if self.x >= 10:
			raise StopIteration

		return self.x ** self.x

	def __iter__(self):
		return self

s = Seq()

for e in s:
	print(e)

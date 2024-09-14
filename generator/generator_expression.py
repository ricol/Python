#!/usr/bin/env python
#-*- coding: utf-8 -*-

def test():
	n = (e for e in range(int(5e7)) if not e % 3)
	i = 0
	for e in n:
		print(e)
		i += 1
		if i > 100:
			raise StopIteration

try:
	test()
except Exception as e:
	print("exception: " + str(e))
print("end")

#!/usr/bin/env python
#-*- coding: utf-8 -*-

def gcd(num1, num2):
	'''this is function to calculate the greatest common divisor of two integers'''
	min = num1 if num1 < num2 else num2
	largest_factor = 1
	for i in range(1, min + 1):
		if num1 % i == 0 and num2 % i == 0: 
			largest_factor = i
	return largest_factor

num1 = int(input('num1?'))
num2 = int(input('num2?'))
f = gcd(num1, num2)
print 'greatest common divisor of %d and %d is: %d' % (num1, num2, f)

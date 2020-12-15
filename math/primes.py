#!/usr/bin/env python
#-*- coding: utf-8 -*-

from math import sqrt

def is_prime(n):
	root = int(round(sqrt(n)) + 1)
	for trial_factor in range(2, root):
		if n % trial_factor == 0:
			return False
	return True

def main():
	max_value = int(input("Display primes up to what value? "))
	for v in range(2, max_value + 1):
		if is_prime(v): print(v)

main()

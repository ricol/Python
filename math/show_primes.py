#!/usr/bin/env python3

from math import sqrt

def is_prime(num):
	print("checking %d..." % num)
	if num <= 1: return False
	if num != 2 and num % 2 == 0: return False

	to = int(round(sqrt(num)) + 1)
	for x in range(3, to, 2):
		if num % x == 0: return False
	return True

if __name__ == "__main__":
	primes = []
	for x in range(2, 100):
		if is_prime(x): primes.append(x)
	print(primes)
	
	product = primes[0]
	for i in range(1, len(primes)):
		print("prime: " + str(primes[i]))
		new_prime = product * primes[i] + 1
		if is_prime(new_prime):
			print("new prime: " + str(new_prime))
		else:
			print(str(new_prime) + " is not prime! [error]")
		product *= primes[i]

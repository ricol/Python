#!/usr/bin/env python
#-*- coding: utf-8 -*-

def factors(n):
    results = []
    for k in range(1, n + 1):
        if n % k == 0:
            results.append(k)
    return results

def factors_generator(n):
    for k in range(1, n + 1):
        if n % k == 0:
            yield k

def factors_improved(n):
    k = 1
    while k * k < n:
        if n % k == 0:
            yield k
            yield n // k
        k += 1
    if k * k == n:
        yield k

def isPrime(n):
    for i in range(2, n / 2):
        if n % i == 0: return False
    return True

if __name__ == "__main__":
    value = int(input("type a number?"))
    print("calculating...")
    print("factors: %s" % factors(value))
    print("factors_generator: %s" % [i for i in factors_generator(value)])
    print("factors_improved: %s" % [i for i in factors_improved(value)])
    print("isPrime: %s" % isPrime(value))

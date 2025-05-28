#!/usr/bin/env python
#-*- coding: utf-8 -*-

from random import randrange

def show_call_and_return_details(f):
    def execute_augmented(x, y):
        call_string = "{}({}, {})".format(f.__name__, x, y)
        print(">>> Calling " + call_string)
        result = f(x, y)
        print("<<< Returning {} from ".format(result) + call_string)
        return result
    return execute_augmented

@show_call_and_return_details
def max(x, y):
    return x if x > y else y

@show_call_and_return_details
def gcd(m, n):
    if n == 0:
        return m
    else:
        return gcd(n, m % n)

@show_call_and_return_details
def summation(begin, end):
    sum = 0
    while begin != end:
        sum += begin
        begin += 1
    return sum

@show_call_and_return_details
def star_rect(length, width):
    for row in range(length):
        print('* ' * width)

max(20, 30)
print("-" * 20)
max(30, 20)
print("-" * 20)
max(20, 20)
print("-" * 20)

gcd(20, 30)
print("-" * 20)
gcd(30, 20)
print("-" * 20)
gcd(20, 20)
print("-" * 20)

summation(20, 30)
print("-" * 20)

star_rect(7, 3)
print("-" * 20)
star_rect(4, 4)
print("-" * 20)
star_rect(2, 5)
print("-" * 20)
print(randrange(10, 21), "is a pseudorandom integer in the range 10 to 20, inclusive")
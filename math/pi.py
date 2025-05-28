#!/usr/bin/env python
#-*- coding: utf-8 -*-

# PI = 4 * (1 / 1 - 1 / 3 + 1 / 5 - 1 / 7 + ...)

def pi(n):
    i = 0
    num = 1.0
    sum = 0
    while i < n:
        sum += (-1) ** i * (1.0 / num)
        i += 1
        num += 2
    return sum * 4

def pi_new(n):
    y = n * 2
    list1 = [1 / x for x in range(1, y, 4)]
    list2 = [-1 / x for x in range(3, y, 4)]
    return (sum(list1) + sum(list2)) * 4   

def pi_new2(n):
    list = [(-1) ** (x + 1) * (1.0 / (x * 2 - 1)) for x in range(1, n)] 
    return sum(list) * 4

NUM = 1000000
i = NUM
print("calculating...using pi")
while i <= NUM + 10:
    print(("n: " + str(i) + " -> pi: " + str(pi(i))))
    i += 1
print("done.")

i = NUM
print("calculating...using pi_new")
while i <= NUM + 10:
    print(("n: " + str(i) + " -> pi: " + str(pi_new(i))))
    i += 1
print("done.")

i = NUM
print("calculating...using pi_new2")
while i <= NUM + 10:
    print(("n: " + str(i) + " -> pi: " + str(pi_new2(i))))
    i += 1
print("done.")
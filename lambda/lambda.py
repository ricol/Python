#!/usr/bin/env python
#-*- coding: utf-8 -*-

# Function definition is here
sum = lambda arg1, arg2: arg1 + arg2;

# Now you can call sum as a function
print("Value of total : ", sum(10, 20))
print("Value of total : ", sum(20, 20))

def process(x):
    return x * x

data = list(range(10))
print([x * x for x in data])
print(list(map(process, data)))

def evaluate(f, x, y):
    return f(x, y)

print(evaluate(lambda x, y: 3 * x + y, 10, 2))
print(evaluate(lambda x, y: 10 if x == y else 2, 5, 5))
print(evaluate(lambda x, y: 10 if x == y else 2, 5, 3))

def multiple_labmdas():
    return [lambda x: i * x for i in range(5)]

def multiple_labmdas_correct():
    return [lambda x, i = i: i * x for i in range(5)]

for l in multiple_labmdas():
    print l(2)

for l in multiple_labmdas_correct():
    print l(2)
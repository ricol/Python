#!/usr/bin/env python
#-*- coding: utf-8 -*-

tup1 = ('physics', 'chemistry', 1997, 2000)
tup2 = (1, 2, 3, 4, 5)
tup3 = "a", "b", "c", "d"

print(tup1)
print(tup2)
print(tup3)

tup1 = ('physics', 'chemistry', 1997, 2000)
tup2 = (1, 2, 3, 4, 5, 6, 7)
print("tup1[0]: ", tup1[0])
print("tup2[1:5]: ", tup2[1:5])

tup1 = (12, 34.56)
tup2 = ('abc', 'xyz')

# Following action is not valid for tuples
# tup1[0] = 100;

# So let's create a new tuple as followsb
tup3 = tup1 + tup2
print(tup3)

tup = ('physics', 'chemistry', 1997, 2000)
print(tup)
del tup
print("After deleting tup : ")
try:
    print(tup)
except:
    print("Not defined!")
finally:
    print("complete")

print('abc', -4.24e93, 18 + 6.6j, 'xyz')
x, y = 1, 2
print("Value of x , y : ", x, y)

tup1 = ('physics', 'chemistry', 1997, 2000)
tup2 = (1, 2, 3, 4, 5, 6, 7)
print("tup1[0]: ", tup1[0])
print("tup2[1:5]: ", tup2[1:5])

tup1 = (12, 34.56)
tup2 = ('abc', 'xyz')

# Following action is not valid for tuples
# tup1[0] = 100;

# So let's create a new tuple as follows
tup3 = tup1 + tup2
print(tup3)

tup = ('physics', 'chemistry', 1997, 2000)
print(tup)

print(list(tup))
del tup
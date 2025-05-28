#!/usr/bin/env python
#-*- coding: utf-8 -*-

import random

'''
this is demonstration of Python language
'''

print("wangxinghe")
print(12.32)
print(True)
print(False)
print(0xff)
print(5.23e10)
print(232.232e-10)

description = '''
Welcome to Python world!
This is a demonstration of basic syntax of Python language.
Feel free to experiment every aspect of Python and enjoy! :)
'''
print(description)

description = """
Welcome to Python world!
This is a demonstration of basic syntax of Python language.
Feel free to experiment every aspect of Python and enjoy! :)
"""
print(description)

str = 'Hello World!'

print(str)  # Prints complete string
print(str[0])  # Prints first character of the string
print(str[2:5])  # Prints characters starting from 3rd to 5th
print(str[2:])  # Prints string starting from 3rd character
print(str * 2)  # Prints string two times
print(str + "TEST")  # Prints concatenated string

counter = 100  # An integer assignment
miles = 1000.0  # A floating point
name = "John"  # A string

print(type(counter))
print(type(miles))
print(type(name))

print(counter)
print(miles)
print(name)

list = ['abcd', 786, 2.23, 'john', 70.2]
tinylist = [123, 'john']

print(list)  # Prints complete list
print(list[0])  # Prints first element of the list
print(list[1:3])  # Prints elements starting from 2nd till 4th
print(list[2:])  # Prints elements starting from 3rd element
print(tinylist * 2)  # Prints list two times
print(list + tinylist)  # Prints concatenated lists

tuple = ('abcd', 786, 2.23, 'john', 70.2)
tinytuple = (123, 'john')

print(tuple)  # Prints complete list
print(tuple[0])  # Prints first element of the list
print(tuple[1:3])  # Prints elements starting from 2nd till 3rd
print(tuple[2:])  # Prints elements starting from 3rd element
print(tinytuple * 2)  # Prints list two times
print(tuple + tinytuple)  # Prints concatenated lists

dict = {}
dict['one'] = "This is one"
dict[2] = "This is two"

tinydict = {'name': 'john', 'code': 6734, 'dept': 'sales'}

print(dict['one'])  # Prints value for 'one' key
print(dict[2])  # Prints value for 2 key
print(tinydict)  # Prints complete dictionary
try:
    print(list(tinydict.keys()))  # Prints all the keys
    print(list(tinydict.values()))  # Prints all the values
except:
    print("Exception!")
finally:
    print("Complete")

s = set()
for _ in range(10):
    s.add(random.randint(0, 10))
print(s)

print(1 ^ 2)
print( ~ 2)
print(1 & 2)
print(1 ^ 2)
print(1 << 2)
print(1 >> 2)
print("positive" if random.randint(1, 10) - 5 > 0 else "negative")
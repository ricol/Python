#!/usr/bin/env python
#-*- coding: utf-8 -*-

dict = {'Name': 'Zara', 'Age': 7, 'Class': 'First'}
print("dict['Name']: ", dict['Name'])
print("dict['Age']: ", dict['Age'])

dict = {'Name': 'Zara', 'Age': 7, 'Class': 'First'}
dict['Age'] = 8
# update existing entry
dict['School'] = "DPS School"
# Add new entry

print("dict['Age']: ", dict['Age'])
print("dict['School']: ", dict['School'])

dict = {'Name': 'Zara', 'Age': 7, 'Class': 'First'}
del dict['Name']
# remove entry with key 'Name'

print("dict['Age']: ", dict['Age'])
# print "dict['School']: ", dict['School']

print("keys:")
print(list(dict.keys()))

dict.clear()
# remove all entries in dict
del dict
# delete entire dictionary

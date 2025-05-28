#!/usr/bin/env python
#-*- coding: utf-8 -*-

name = "ricol"
age = 35
gender = "male"
print("welcome")
print(("name: ", name, " age: ", age, " gender: ", gender))
print(f'welcome name: {name}, age: {age}, gender: {gender}')
print(f"welcome name: {name}, age: {age:.3f}, gender: {gender}")
print(("welcome name: {0}, age: {1:03d}, gender: {2}".format(name, age, gender)))
print(("welcome name: %s, age: %d, gender: %s" % (name, age, gender)))
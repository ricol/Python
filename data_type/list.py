#!/usr/bin/env python
#-*- coding: utf-8 -*-

list1 = ['physics', 'chemistry', 1997, 2000]
list2 = [1, 2, 3, 4, 5]
list3 = ["a", "b", "c", "d"]

print(list1)
print(list2)
print(list3)

list1 = ['physics', 'chemistry', 1997, 2000]
list2 = [1, 2, 3, 4, 5, 6, 7]
print("list1[0]: ", list1[0])
print("list2[1:5]: ", list2[1:5])

list = ['physics', 'chemistry', 1997, 2000]
print("Value available at index 2 : ")
print(list[2])
list[2] = 2001
print("New value available at index 2 : ")
print(list[2]) 

list1 = ['physics', 'chemistry', 1997, 2000]
print(list1)
del list1[2]
print("After deleting value at index 2 : ")
print(list1)

def capitalize_all(t):
    res = []
    for s in t:
        res.append(s.capitalize())
    return res

names = ['ricol', 'wang', 'qian', 'chun', 'yan']
print(names)
print((capitalize_all(names)))

def capitalize_all_new(t):
    return [s.capitalize() for s in t]

names = ['ricol', 'wang', 'qian', 'chun', 'yan']
print(names)
print((capitalize_all_new(names)))

def only_upper(t):
    res = []
    for s in t:
        if s.isupper():
            res.append(s)
    return res

names = ['ricol', 'WANG', 'xing', 'HE']
print(names)
print((only_upper(names)))

def only_upper_new(t):
    return [s for s in t if s.isupper()]

names = ['ricol', 'WANG', 'xing', 'HE']
print(names)
print((only_upper_new(names)))

print((any([False, False, False])))
print((any([True, False, False])))
print((all([False, False, False])))
print((all([True, False, False])))
print((all([True, True, True])))

list1 = ['physics', 'chemistry', 1997, 2000]
list2 = [1, 2, 3, 4, 5, 6, 7]
print("list1[0]: ", list1[0])
print("list2[1:5]: ", list2[1:5])

list = ['physics', 'chemistry', 1997, 2000]
print("Value available at index 2 : ")
print(list[2])
list[2] = 2001
print("New value available at index 2 : ")
print(list[2])

list1 = ['physics', 'chemistry', 1997, 2000]
print(list1)
del list1[2]
print("After deleting value at index 2 : ")
print(list1)

T = [[11, 12, 5, 2], [15, 6, 10], [10, 8, 12, 5], [12, 15, 8, 6]]
print(tuple(T))
T[2] = [11, 9]
T[0][3] = 7
for r in T:
    for c in r:
        print(c)
    print()

def list_copy(lst):
    result = []
    for i in lst:
        result += [i]
    return result

def main():
    a = [1, 2, 3, 4, 5]
    b = list_copy(a)
    print("a = ", a, " b = ", b)
    print("Is ", a, " equal to ", b, "?")
    print(a == b)
    print("Are ", a, " and ", b, " aliases?")
    print(a is b)
    b[2] = 10
    print("a = ", a, " b = ", b)

main()

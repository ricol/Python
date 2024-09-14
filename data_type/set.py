#!/usr/bin/env python
#-*- coding: utf-8 -*-

import random as random

Days = set(["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"])
Months = {"Jan", "Feb", "Mar"}
Dates = {21, 22, 17}
print(Days)
print(Months)
print(Dates)

Days = set(["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"])

for d in Days:
    print(d)

Days = set(["Mon", "Tue", "Wed", "Thu", "Fri", "Sat"])

Days.add("Sun")
print(Days)

Days = set(["Mon", "Tue", "Wed", "Thu", "Fri", "Sat"])

Days.discard("Sun")
print(Days)

DaysA = set(["Mon", "Tue", "Wed"])
DaysB = set(["Wed", "Thu", "Fri", "Sat", "Sun"])
AllDays = DaysA | DaysB
print(AllDays)

DaysA = set(["Mon", "Tue", "Wed"])
DaysB = set(["Wed", "Thu", "Fri", "Sat", "Sun"])
AllDays = DaysA & DaysB
print(AllDays)

DaysA = set(["Mon", "Tue", "Wed"])
DaysB = set(["Wed", "Thu", "Fri", "Sat", "Sun"])
AllDays = DaysA - DaysB
print(AllDays)

DaysA = set(["Mon", "Tue", "Wed"])
DaysB = set(["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"])
SubsetRes = DaysA <= DaysB
SupersetRes = DaysB >= DaysA
print(SubsetRes)
print(SupersetRes)

a = set()
b = set()
for i in range(10):
    a.add(random.randint(1, 10))
    b.add(random.randint(1, 10))
print(a)
print(b)
print(a | b)
print(a - b)
print(a ^ b)

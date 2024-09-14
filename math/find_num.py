#!/usr/bin/env python
#-*- coding: utf-8 -*-

import os

num = int(os.sys.argv[1])
total = yes = no = 0
for n in range(1, num + 1):
    nums = [x for x in range(1, (n / 2) + 1) if n % x  == 0]
    s = sum(nums)
    total += 1
    if s == n:
        yes += 1
        print("Find %d ... %s -> sum: %d" % (n, nums, s))
    else:
        no += 1
print("Find: %d" % yes)
print("Total: %d" % total)

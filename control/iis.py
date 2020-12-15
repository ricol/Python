#!/usr/bin/env python
#-*- coding: utf-8 -*-

import random

num = int(random.random() * 10)
print(num)
print("Hello" if num > 5 else "Hi")

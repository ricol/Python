#!/usr/bin/env python
#-*- coding: utf-8 -*-

import random

for i in range(10):
    print('Beginning of loop iteration %d' % i)
    try:
        r = random.randint(1, 3)
        if r == 1:
            print(int('Fred'))
        elif r == 2:
            [][2] = 5
        else:
            print(3 / 0)
    except ValueError as e:
        print("Can not convert integer: %s" % e)
    except IndexError as e:
        print("List index is out of range: %s" % e)
    except ZeroDivisionError as e:
        print("Division by zero not allowed: %s" % e)
    print("End of loop iteration %d" % i)
print("complete.")

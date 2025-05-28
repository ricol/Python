#!/usr/bin/env python
#-*- coding: utf-8 -*-

import random

def producer():
  while True:
    data = random.randint(0, 9)
    print("producing...", data)
    yield data

def consumer():
  count = 0
  while True:
    count += 1
    print("consumer...%d..." % count)
    data = yield
    print("consumed...", data)

def clerk(jobs, producer, consumer):
  print('execute () times of production and consumption'.format(jobs))
  p = producer()
  c = consumer()
  next(c)
  for i in range(jobs):
    data = next(p)
    c.send(data)

if __name__ == "__main__":
  clerk(10, producer, consumer)
  print("end main.")
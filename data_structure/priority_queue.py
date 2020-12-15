#!/usr/bin/env python
#-*- coding: utf-8 -*-

def heapify(arr, n, i):
	largest = i
	l = 2 * i + 1
	r = 2 * i + 2

	if l < n and arr[largest] < arr[l]:
		largest = l

	if r < n and arr[largest] < arr[r]:
		largest = r

	if largest != i:
		arr[i], arr[largest] = arr[largest], arr[i]
		heapify(arr, n, largest)

def insert(arr, newNum):
	size = len(arr)
	if size == 0:
		arr.append(newNum)
	else:
		arr.append(newNum)
		for i in range((size // 2) - 1, -1, -1):
			heapify(arr, size, i)

def deleteNode(array, num):
	size = len(array)
	i = 0
	for i in range(0, size):
		if num == array[i]:
			break

	array[i], array[size - 1] = array[size - 1], array[i]

	array.remove(size - 1)

	for i in range((len(array) // 2) - 1, -1, -1):
		heapify(array, len(array), i)

arr = []
insert(arr, 3)
insert(arr, 4)
insert(arr, 9)
insert(arr, 5)
insert(arr, 2)

print("max-heap array: " + str(arr))
deleteNode(arr, 4)
print("after deleting an element: " + str(arr))

class _PriorityQEntry:

	def __init__(self, item, priority):
		self.item = item
		self.priority = priority

class PriorityQueue:

	def __init__(self):
		self._qList = list()

	def isEmpty(self):
		return len(self) == 0

	def __len__(self):
		return len(self._qList)

	def enqueue(self, item, priority):
		entry = _PriorityQEntry(item, priority)
		self._qList.append(entry)

	def dequeue(self):
		highest = 0
		for i in range(len(self)):
			if self._qList[i].priority < self._qList[highest].priority:
				highest = i
		entry = self._qList[highest]
		self._qList.pop(highest)
		return entry.item, entry.priority

import random

q = PriorityQueue()
LEN = 10

for i in range(LEN):
	num = i
	p = random.randint(0, LEN)
	print("enqueue...%d[%d]" % (num, p))
	q.enqueue(num, p)

while not q.isEmpty():
	item, priority = q.dequeue()
	print "item: %d[%d]" % (item, priority)

class Queue:

	def __init__(self):
		self.data = []

	def enqueue(self, item):
		self.data.append(item)

	def dequeue(self):
		return self.data.pop(0)

	def __len__(self):
		return len(self.data)

	def is_empty(self):
		return len(self) == 0

q = Queue()
for i in range(LEN):
	item = random.randint(0, LEN)
	print("enqueue...%d" % item)
	q.enqueue(item)
while not q.is_empty():
	item = q.dequeue()
	print item 

class BPriorityQueue:

	def __init__(self, max_priority):
		self._qSize = 0
		self._qLevels = [Queue() for _ in range(max_priority)]

	def is_empty(self):
		return len(self) == 0

	def __len__(self):
		return self._qSize

	def enqueue(self, item, priority):
		self._qSize += 1
		self._qLevels[priority].enqueue(item)

	def dequeue(self):
		if self.is_empty():
			return None

		i = 0
		while i < len(self._qLevels) and self._qLevels[i].is_empty():
			i += 1
		self._qSize -= 1
		return self._qLevels[i].dequeue(), i

q = BPriorityQueue(11)
LEN = 10

for i in range(LEN):
	num = i
	p = random.randint(0, LEN)
	print("enqueue...%d[%d]" % (num, p))
	q.enqueue(num, p)

while not q.is_empty():
	item, priority = q.dequeue()
	print "item: %d[%d]" % (item, priority)

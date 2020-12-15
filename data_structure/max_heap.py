#!/usr/bin/env python
#-*- coding: utf-8 -*-

import funs

class MaxHeap:

	def __init__(self, maxSize):
		self._elements = [0 for _ in range(maxSize)]
		self._count = 0

	def __len__(self):
		return self._count

	def capacity(self):
		return len(self._elements)

	def add(self, value):
		assert self._count < self.capacity(), "Can not add to a full heap"
		self._elements[self._count] = value
		self._count += 1
		self._siftUp(self._count - 1)

	def extract(self):
		assert self._count > 0, "Can not extract from an empty heap"
		value = self._elements[0]
		self._count -= 1
		self._elements[0] = self._elements[self._count]
		self._siftDown(0)
		return value

	def _siftUp(self, ndx):
		if ndx > 0:
			parent = ndx // 2
			if self._elements[ndx] > self._elements[parent]:
				self._elements[ndx], self._elements[parent] = self._elements[parent], self._elements[ndx]
				self._siftUp(parent)

	def _siftDown(self, ndx):
		left = 2 * ndx + 1
		right = left + 1
		largest = ndx
		if left < self._count and self._elements[left] >= self._elements[largest]:
			largest = left
		elif right < self._count and self._elements[right] >= self._elements[largest]:
			largest = right
		if largest != ndx:
			self._elements[ndx], self._elements[largest] = self._elements[largest], self._elements[ndx]
			self._siftDown(largest)

	def __str__(self):
		return str(self._elements)

	def show(self):
		s = []
		q = []
		q.append(0)
		while len(q) > 0:
			i = q.pop(0)
			l = i * 2 + 1
			r = l + 1
			s.append(str(self._elements[i]))
			if l < self.capacity(): q.append(l)
			if r < self.capacity(): q.append(r)
		print ",".join(s)

	def __iter__(self):
		self._index = 0
		return self

	def next(self):
		self._index += 1
		if self._index - 1 < len(self._elements):
			return self._elements[self._index - 1]
		raise StopIteration()

def simpleHeapSort(data):
	n = len(data)
	heap = MaxHeap(n)
	for item in data:
		heap.add(item)

	for i in range(n - 1, -1, -1):
		data[i] = heap.extract()

if __name__ == "__main__":
	LEN = 100
	heap = MaxHeap(LEN)
	import random
	for _ in range(LEN):
		heap.add(random.randint(0, LEN))
	print heap
	heap.show()
	print "verify..." + str(funs.isHeap(heap._elements, 0))
	data = []
	print "generating data..."
	for _ in range(LEN):
		data.append(random.randint(0, LEN))
	print "sorting..."
	simpleHeapSort(data)
	print "complete"
	print "is sorted..." + str(funs.isSorted(data))

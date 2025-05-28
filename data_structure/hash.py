#!/usr/bin/env python
#-*- coding: utf-8 -*-

class _MapEntry:

    def __init__(self, key, value):
        self.key = key
        self.value = value

class HashMap:

    def __init__(self, capacity = 10):
        self._table = [None for _ in range(capacity)]
        self._count = 0
        self._maxCount = len(self._table) - len(self._table) // 3

    def __len__(self):
        return self._count

    def __contains__(self, key):
        return self._locateSlot(key) is not None 

    def __setitem__(self, key, value):
        slot = self._locateSlot(key)
        if slot == None:
            slot = self._findNewSlot(key)

        self._table[slot] = _MapEntry(key, value)
        self._count += 1
        if self._count >= self._maxCount:
            self._rehash()

    def __getitem__(self, key):
        slot = self._locateSlot(key)
        if slot is not None:
            return self._table[slot].value
        return None

    def remove(self, key):
        slot = self._locateSlot(key)
        if slot is not None: 
            self._table[slot] = None

    def __iter__(self):
        self._index = 0
        return self

    def next(self):
        self._index += 1
        while self._index < len(self._table) and self._table[self._index] == None: 
            self._index += 1
        if self._index >= len(self._table): raise StopIteration()
        data = self._table[self._index]
        return data.key, data.value

    def _locateSlot(self, key):
        slot = self._hash1(key)
        step = self._hash2(key)

        while self._table[slot] is not None and self._table[slot].key != key:
            slot = (slot + step) % len(self._table)

        if self._table[slot] is None: return None

        # print("_locateSlot for key: %s -> slot: %d" % (key, slot))
        return slot

    def _findNewSlot(self, key):
        slot = self._hash1(key)
        step = self._hash2(key)

        while self._table[slot] is not None:
            slot = (slot + step) % len(self._table)

        # print("_findNewSlot for key: %s -> slot: %d" % (key, slot))
        return slot

    def _rehash(self):
        oriTable = self._table
        newSize = len(self._table) * 2 + 1
        self._table = [None for _ in range(newSize)]
        self._count = 0
        self._maxCount = newSize - newSize // 3

        for entry in oriTable:
            if entry is not None:
                slot = self._findNewSlot(entry.key)
                self._table[slot] = entry
                self._count += 1

    def _hash1(self, key):
        return abs(hash(key) % len(self._table))

    def _hash2(self, key):
        return 1

if __name__ == "__main__":
    h = HashMap()
    h["wangxinghe"] = 37
    h["ricolwang"] = 30
    h["star"] = 20
    h["wang"] = 20
    print h["wangxinghe"]
    print h["ricolwang"]
    print h["star"]
    print h["wang"]
    print h["hi"]
    h["wang"] = 10
    print h["wang"]

    for i in range(100):
        key = 'key' + str(i)
        value = i
        print "set h[%s]=%d" % (key, value)
        h[key] = value

    for k, v in h:
        print "h[%s]=%d" % (k, v)
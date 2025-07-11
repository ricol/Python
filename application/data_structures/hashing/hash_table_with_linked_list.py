#!/usr/bin/env python
#-*- coding: utf-8 -*-

from collections import deque
from hash_table import HashTable

class HashTableWithLinkedList(HashTable):
    def __init__(self, * args, ** kwargs):
        super().__init__(*args, ** kwargs)

    def _set_value(self, key, data):
        self.values[key] = deque([]) if self.values[key] is None else self.values[key]  
        self.values[key].appendleft(data)
        self._keys[key] = self.values[key]

    def balanced_factor(self):
        return sum([self.charge_factor - len(slot) for slot in self.values])\
            / self.size_table * self.charge_factor

    def _colision_resolution(self, key, data=None):
        if not (len(self.values[key]) == self.charge_factor
                and self.values.count(None) == 0):
            return key
        return super()._colision_resolution(key, data)
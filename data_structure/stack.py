#!/usr/bin/env python
#-*- coding: utf-8 -*-

class Stack:
    def __init__(self):
        self.stack = []

    def add(self, dataval):
        # Use list append method to add element
        if dataval not in self.stack:
            self.stack.append(dataval)
            return True
        else:
            return False

# Use peek to look at the top of the stack

    def peek(self):
        return self.stack[0]

AStack = Stack()
AStack.add("Mon")
AStack.add("Tue")
AStack.peek()
print((AStack.peek()))
AStack.add("Wed")
AStack.add("Thu")
print((AStack.peek()))

class Stack1:
    def __init__(self):
        self.stack = []

    def add(self, dataval):
        # Use list append method to add element
        if dataval not in self.stack:
            self.stack.append(dataval)
            return True
        else:
            return False

# Use list pop method to remove element

    def remove(self):
        if len(self.stack) <= 0:
            return ("No element in the Stack")
        else:
            return self.stack.pop()

AStack = Stack1()
AStack.add("Mon")
AStack.add("Tue")
print((AStack.remove()))
AStack.add("Wed")
AStack.add("Thu")
print((AStack.remove()))
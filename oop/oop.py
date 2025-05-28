#!/usr/bin/env python
#-*- coding: utf-8 -*-

class Publication:

	def __init__(self, code, title, author):
		self._code = code
		self._title = title
		self._author = author

	def getCode(self):
		return self._code

	def getBibEntry(self):
		return '[' + self.getCode() + ']' + self._title + ' by ' + self._author

	def __str__(self):
		return 'code: ' + str(self._code) + ', title: ' + str(self._title) + ', author: ' + str(self._author)

class Book(Publication):

	def __init__(self, code, title, author, publisher, year):
		super().__init__(code, title, author)
		self._publisher = publisher
		self._year = year

	def getBibEntry(self):
		return super().getBibEntry() + ', ' + self._publisher + ', ' + self._year

	def __str__(self):
		return (super().__str__()) + ', publisher: ' + str(self._publisher) + ', year: ' + str(self._year)

p = Publication('Test80', 'Just a test', 'Rob Green')
b = Book('Smith90', 'The year that was', 'John Smith', 'Bookends Publishing', 1990)
print(p)
print(b)
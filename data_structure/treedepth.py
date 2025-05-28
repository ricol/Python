#!/usr/bin/env python
#-*- coding: utf-8 -*-

def tree(height):
	"""
	Draws a tree of a given height.
	"""
	row = 0
	while row < height:
		count = 0
		while count < height - row:
			print(end=' ')
			count += 1
		count = 0
		while count < 2 * row - 1:
			print(end='*')
			count += 1
		print()
		row += 1

def main():
	"""Allows users to draw tress of various heights"""
	height = int(input('Enter height of tree: '))
	tree(height)

if __name__ == "__main__":
	main()
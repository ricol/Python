#!/usr/bin/env python
#-*- coding: utf-8 -*-

import sys

def main():
	if len(sys.argv) < 2:
		print("Usage: python wordcount <filename>")
		print("       where <filename> is the name of a text file.")
	else:
		filename = sys.argv[1]
		counters = {}
		with open(filename, 'r') as f:
			content = f.read()
			words = content.split()
			for word in words:
				word = word.upper()
				if word not in counters:
					counters[word] = 1
				else:
					counters[word] += 1
			for word, count in counters.items():
				print(word, count)

if __name__ == "__main__":
	main()

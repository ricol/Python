#!/usr/bin/env python
#-*- coding: utf-8 -*-

import os

def directory_size(path):
	total = 0
	for root, dirs, files in os.walk(path):
		for file in files:
			file_path = os.path.join(root, file)
			if os.path.isfile(file_path):
				total += os.path.getsize(file_path)
	return total

def format_bytes(size_in_bytes):
	units = ['B', 'KB', 'MB', 'GB']
	i = 0
	while size_in_bytes >= 1024 and i < len(units) - 1:
		size_in_bytes /= 1024
		i += 1
	return f"{size_in_bytes:.2f} {units[i]}"

def getAllSubdirs(directory, all):
	for f in os.listdir(directory):
		dir = os.path.join(directory, f)
		if os.path.isdir(dir):
			if f.endswith('.git'):
				all.append(dir)
			else:
				getAllSubdirs(dir, all)

if __name__ == '__main__':
	import sys

	if len(sys.argv) < 2:
		print("Usage: cleanupgit.py <directory> <size=10000000>")
		sys.exit()

	oversize = 10 * 1024 * 1024
	directory = sys.argv[1]

	if len(sys.argv) >= 3:
		oversize = int(sys.argv[2])

	print("%s: searching..." % directory)
	all_git_dirs = []
	getAllSubdirs(directory, all_git_dirs)
	print("analyzing...")

	for git_dir in all_git_dirs:
		size = directory_size(git_dir)
		if size >= oversize:
			print(f"{git_dir} [{format_bytes(size)}]")
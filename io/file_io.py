#!/usr/bin/env python
#-*- coding: utf-8 -*-

import sys

file_name = 'test.dat'
file_finish = 'finish'
file_text = ''

try:
    # open file stream
    file = open(file_name, "w")

except IOError:
    print(("There was an error writing to", file_name))
    sys.exit()
print((
      "Enter '",
      file_finish,
      ))
print("' When finished")
while file_text != file_finish:
    file_text = eval(input("Enter text: "))
    if file_text == file_finish:
        # close the file
        file.close
        break
    file.write(file_text)
    file.write("\n")
file.close()
file_name = eval(input("Enter filename: "))
if len(file_name) == 0:
    print("Next time please enter something")
    sys.exit()

try:
    file = open(file_name, "r")

except IOError:
    print("There was an error reading file")
    sys.exit()
file_text = file.read()
file.close()
print(file_text)
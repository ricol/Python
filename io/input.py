#!/usr/bin/env python
#-*- coding: utf-8 -*-

import random

def input_number(msg=""):
    while True:
        try:
            num = int(input(msg + "\n"))
            return num
        except Exception:
            print("Invalid number! Try again")

NUM = int(random.random() * 100)
print("Please guess the number?")
guess = int(input())
while True: 
    if guess < NUM:
        guess = input_number("Not correct! Large number! Please guess?")
    elif guess > NUM:
        guess = input_number("Not correct! Smaller number! Please guess?")
    else:
        break
print("You made it. The correct number is: %d" % NUM)
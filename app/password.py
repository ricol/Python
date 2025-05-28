#!/usr/bin/env python
#-*- coding: utf-8 -*-

import hashlib
import uuid

def hash_password(password):
    # userid is used to generate a random number
    salt = uuid.uuid4().hex  #salt is stored in hexadecimal value
    return hashlib.sha256(salt.encode() + password.encode()).hexdigest() + ':' + salt

def check_password(hashed_password, user_password):
    # hexdigest is used as an algorithm for storing passwords
    password, salt = hashed_password.split(':')
    return password == hashlib.sha256(salt.encode() + user_password.encode()).hexdigest()

new_pass = input('Please enter required password ')
hashed_password = hash_password(new_pass)
print(('The string to store in the db is: ' + hashed_password))
old_pass = input('Re-enter new password ')

if check_password(hashed_password, old_pass):
    print('Yuppie!! You entered the right password')
else:
    print('Oops! I am sorry but the password does not match')
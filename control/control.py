#!/usr/bin/env python
#-*- coding: utf-8 -*-

var = 100
if (var == 100): print("Value of expression is 100")
print("Good bye!")

var1 = 100
if var1:
    print("1 - Got a true expression value")
    print(var1)

var2 = 0
if var2:
    print("2 - Got a true expression value")
    print(var2)
print("Good bye!")

var = 100
if var == 200:
    print("1 - Got a true expression value")
    print(var)
elif var == 150:
    print("2 - Got a true expression value")
    print(var)
elif var == 100:
    print("3 - Got a true expression value")
    print(var)
else:
    print("4 - Got a false expression value")
    print(var)

print("Good bye!")

var = 100
if var < 200:
    print("Expression value is less than 200")
    if var == 150:
        print("Which is 150")
    elif var == 100:
        print("Which is 100")
    elif var == 50:
        print("Which is 50")
    elif var < 50:
        print("Expression value is less than 50")
else:
    print("Could not find true expression")

print("Good bye!")

count = 0
while (count < 9):
    print('The count is:', count)
    count = count + 1

print("Good bye!")

count = 0
while count < 5:
    print(count, " is  less than 5")
    count = count + 1
else:
    print(count, " is not less than 5")

    for letter in 'Python':  # First Example
        print('Current Letter :', letter)

print("Good bye!")

fruits = ['banana', 'apple', 'mango']
for fruit in fruits:
    print(('Current fruit :', fruit))

fruits = ['banana', 'apple', 'mango']
for index in range(len(fruits)):
    print('Current fruit :', fruits[index])

print("Good bye!")

for num in range(10, 20):  #to iterate between 10 to 20
    for i in range(2, num):  #to iterate on the factors of the number
        if num % i == 0:  #to determine the first factor
            j = num / i  #to calculate the second factor
            print('%d equals %d * %d' % (num, i, j))
            break  #to move to the next number, the #first FOR
        else:  # else part of the loop
            print(num, 'is a prime number')

i = 2
while (i < 100):
    j = 2
    while (j <= (i / j)):
        if not (i % j): break
        j = j + 1
    if (j > i / j): print(i, " is prime")
    i = i + 1

print("Good bye!")

for letter in 'Python':  # First Example
    if letter == 'h':
        break
    print('Current Letter :', letter)

var = 10  # Second Example
while var > 0:
    print('Current variable value :', var)
    var = var - 1
    if var == 5:
        break

print("Good bye!")

for letter in 'Python':  # First Example
    if letter == 'h':
        continue
    print('Current Letter :', letter)

var = 10  # Second Example
while var > 0:
    var = var - 1
    if var == 5:
        continue
    print('Current variable value :', var)
print("Good bye!")

for letter in 'Python':
    if letter == 'h':
        pass
        print('This is pass block')
    print('Current Letter :', letter)

print("Good bye!")

name = "ricol"
print(("You are Ricol!" if name == 'ricol' else "I don't know you!"))

for k, v in [("ricol", "wang"), ("xinghe", "wang"), ("chunyan", "qian"), ("jing", "wang")]:
    print("%s -> %s" % (k, v))

for v in ["ricol", "wang", "xing", "he"]:
    print("%s" % v)

print('end.')
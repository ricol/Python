#!/usr/bin/env python
#-*- coding: utf-8 -*-

def psychologist():
    print("Please tell me your problems")
    while True:
        print("Your answer?")
        answer = yield
        print("Got your answer.")
        if answer is not None:
            if answer.endswith("?"):
                print("Don't ask yourself too much questions.")
            elif "good" in answer:
                print("That's good, go on")
            elif "bad" in answer:
                print("Don't be so negative")

free = psychologist()
print(type(free))
free.next()
# print(free.next())
# print(free.next())
# print(free.next())
free.send("I feel bad")
free.send("Why I shouldn't?")
free.send("OK then, I should find what is good for me")

def my_generator():
    try:
        yield 'something'
    except ValueError:
        yield 'dealing with the exception'
    finally:
        print "Ok let's clean"

gen = my_generator()
print(gen.next())
print(gen.throw(ValueError('mean mean mean')))
gen.close()

print(range(10))
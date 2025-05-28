#!/usr/bin/env python
#-*- coding: utf-8 -*-

def scope_test():
    def do_local():
        spam = "local spam"

    def do_nonlocal():
        spam = "nonlocal spam"

    def do_global():
        global spam
        spam = "global spam"

    spam = "test spam"
    do_local()
    print(("After local assignment:", spam))
    do_nonlocal()
    print(("After nonlocal assignment:", spam))
    do_global()
    print(("After global assignment:", spam))

scope_test()
print(("In global scope:", spam))

#!/usr/bin/python

Money = 2000
def AddMoney():
    # Uncomment the following line to fix the code:
    # global Money
        print("incorrect version...")
        try:
            Money = Money + 1
        except:
            print("exception happened!")
        finally:
            pass

print(Money)
AddMoney()
print(Money)

Money = 2000
def AddMoneyFixed():
    # Uncomment the following line to fix the code:
        print("correct version...")
        global Money
        try:
            Money = Money + 1
        except:
            print("exception happened!")
        finally:
            pass

print(Money)
AddMoneyFixed()
print(Money)
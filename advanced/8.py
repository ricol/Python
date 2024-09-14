#!/usr/bin/env python
#-*- coding: utf-8 -*-

class ObjectCreator(object):
    pass

print(ObjectCreator)
# 你可以打印一个类，因为它其实也是一个对象
def echo(o):
    print(o)

echo(ObjectCreator)

# 你可以将类做为参数传给函数
print(hasattr(ObjectCreator, 'new_attribute'))
ObjectCreator.new_attribute = 'foo'
#  你可以为类增加属性
print(hasattr(ObjectCreator, 'new_attribute'))
print(ObjectCreator.new_attribute)
ObjectCreatorMirror = ObjectCreator
# 你可以将类赋值给一个变量
print(ObjectCreatorMirror())

def choose_class(name):
    if name == 'foo':
        class Foo(object):
            pass
        return Foo     
# 返回的是类，不是类的实例
    else:
        class Bar(object):
            pass
        return Bar
MyClass = choose_class('foo')
print(MyClass)              
# 函数返回的是类，不是类的实例>>> print MyClass()            
# 你可以通过这个类创建类实例，也就是对象
# <__main__.foo object="" at="" 0x89c6d4c="">

print(type(1))
print(type("1"))
print(type(ObjectCreator))
print(type(ObjectCreator()))

class MyShinyClass(object):
    pass

MyShinyClass = type('MyShinyClass', (), {})  
# 返回一个类对象
print(MyShinyClass)
print(MyShinyClass())  
#  创建一个该类的实例
# <__main__.myshinyclass object="" at="" 0x8997cec="">
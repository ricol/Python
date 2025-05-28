#!/usr/bin/env python
#-*- coding: utf-8 -*-

class Student(object):

    @property
    def birth(self):
        return self._birth

    @birth.setter
    def birth(self, value):
        self._birth = value

    @property
    def age(self):
        return 2015 - self._birth

class Screen(object):

    @property
    def resolution(self):
        return self.width * self.height

    @resolution.setter
    def resolution(self, value):
        self._resolution = value

s = Screen()
s.width = 1024
s.height = 768
print('resolution =', s.resolution)
if s.resolution == 786432:
    print('测试通过!')
else:
    print('测试失败!')
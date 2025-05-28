#!/usr/bin/env python
#-*- coding: utf-8 -*-

"""DO NOT REMOVE THIS HEADER

BSD License: http://www.opensource.org/licenses/bsd-license.php

Copyright (c) 2008, Sun Microsystems, Inc
All rights reserved.

Redistribution and use in source and binary forms, with or without modification,
are permitted provided that the following conditions are met:

1.Redistributions of source code must retain the above copyright notice,
this list of conditions and the following disclaimer.

2.Redistributions in binary form must reproduce the above copyright notice,
this list of conditions and the following disclaimer in the documentation and/or
 other materials provided with the distribution.

3.Neither the name of the Sun Microsystems, Inc nor the names of its contributors may
be used to endorse or promote products derived from this software without
specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE
FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

"""

# Demonstrate usage of Java Swing classes in Jython

from java.awt import BorderLayout
from javax import swing

__author__ = "Amit Saha <amitksaha@netbeans.org>"
__date__ = "$29 Nov, 2008 12:59:25 AM$"

class SimpleFrame():
    def __init__(self):
        """We shall create the JFrame with a label and a button"""
        print("Initializing")

    def draw(self):
        #Create a JFrame and add a label, button and a menu bar
        self.frame = swing.JFrame("Hello Swing from Python", visible=1)
        # a JLabel
        self.label = swing.JLabel("This is a Swing app in Jython")
        # a JButton
        self.button = swing.JButton("Click me!")
        # Adding a action
        self.button.actionPerformed = self.ClickBtn
        self.frame.contentPane.add(self.label, BorderLayout.CENTER)
        self.frame.contentPane.add(self.button, BorderLayout.SOUTH)
        self.frame.defaultCloseOperation = swing.JFrame.EXIT_ON_CLOSE
        self.frame.pack()

    def ClickBtn(self, event):
        """handle button click"""
        self.label.setText("Clicked!")

if __name__ == '__main__':
    frame = SimpleFrame()
    frame.draw()
#!/usr/bin/env python
#-*- coding: utf-8 -*-

import turtle

turtle.pencolor('red')
turtle.penup()
turtle.setposition(-45, 100)
turtle.pendown()
for i in range(8):
	turtle.forward(80)
	turtle.right(45)
distance = 0.2
angle = 40
turtle.pencolor('blue')
turtle.penup()
turtle.setposition(0, 0)
turtle.pendown()
for i in range(100):
	turtle.forward(distance)
	turtle.left(angle)
	distance += 0.5
turtle.hideturtle()
turtle.exitonclick()
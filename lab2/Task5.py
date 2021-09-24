from random import *
import turtle
import math
turtle.hideturtle()
turtle.speed(100)
turtle.turtlesize(1)
turtle.penup()
turtle.goto(-200, -200)
turtle.pendown()

for i in range (4):
    turtle.forward(400)
    turtle.left(90);
numbers = 6
steps = 200

x = [randint(-180, 180) for i in range(numbers)]
y = [randint(-180, 180) for i in range(numbers)]
u_x = [randint(-3, 3) for i in range(numbers)]
u_y = [randint(-3, 3) for i in range(numbers)]

pool = [turtle.Turtle(shape='circle') for i in range(numbers)]
for unit in pool:
    unit.turtlesize(0.5)
turtle_num = 0
for unit in pool:
    unit.penup()
    unit.goto(x[turtle_num], y[turtle_num])
    turtle_num = turtle_num + 1

for i in range(steps):
    turtle_num = 0
    for unit in pool:
        unit.goto(x[turtle_num], y[turtle_num])
        x[turtle_num] = x[turtle_num] + u_x[turtle_num]
        y[turtle_num] = y[turtle_num] + u_y[turtle_num]
        unit.goto(x[turtle_num], y[turtle_num])
        if x[turtle_num] > 196 or x[turtle_num] < -196:
            u_x[turtle_num] = -u_x[turtle_num]
            x[turtle_num] = x[turtle_num] + u_x[turtle_num]
            unit.goto(x[turtle_num], y[turtle_num])
        if y[turtle_num] > 196 or y[turtle_num] < -196:
            u_y[turtle_num] = -u_y[turtle_num]
            y[turtle_num] = y[turtle_num] + u_y[turtle_num]
            unit.goto(x[turtle_num], y[turtle_num])
        turtle_num = turtle_num + 1
        
        
        

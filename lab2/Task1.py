import turtle
from random import *

turtle.speed('fast')
for step in range(100):
    turtle.forward(randint(1, 30))
    x = randint(1, 2)
    if x == 1:
        turtle.left(randint(1, 180))
    else:
        turtle.right(randint(1, 180))
    

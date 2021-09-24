import turtle

turtle.shape('circle')
turtle.shapesize(0.1)
turtle.goto(200, 0)
turtle.goto(-200, 0)

x = -200
y = 0
ux = 0.7
uy = 1
g = 0.01

steps = 6

for i in range(steps):
    time = int(uy/g)
    for i in range(int(2*time)):
        x = x + ux;
        y = y + uy - g/2
        turtle.goto(x, y)
        uy = uy - g
    uy = -3*uy/4
    ux = max(ux-uy/3, 0)
    
    
